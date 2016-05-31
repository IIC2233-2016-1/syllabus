import functools as fct
import re
import database as db
import evaluations as eva
import helper as hpr
import manipulation as man
import collections as col

# ------------------------TESTING PURPOSE------------------------------------- #
# Toggle TESTING to log methods
TESTING = False

# ---------------------------------------------------------------------------- #


def get_consults(fname):
    # Read consultas.txt
    f = open(fname, 'r')
    # First line is the number of tables
    tb_num = int(f.readline().strip())
    tbs = [db.read_table(f.readline().strip()) for i in range(tb_num)]
    tbs = {tname: tb for tname, tb in tbs}
    # Next line is the number of queries
    # Assumes that each line is one complete query
    query_num = int(f.readline().strip())
    consults = [f.readline().strip() for i in range(query_num)]
    # close file
    f.close()
    return tbs, consults


# The order matters since you want to look for <= before = since = is
# a substring
COL = [' TODO ']
ROW = ['SOLO']
KWS = ['EMPRESTA ', ' DE ', ' ONDE ', ' AGRUPATELOS X ', ' TENIENDO ',
       ' ORDENATELOS X ', ' SOLO ', ' UNETELO CN ']
SET = [' UNETELO CN ', ' UNETELO TODO CN ', ' COMUN CN ', ' SACALE ']


@hpr.log_method(TESTING)
def check_query(query):
    # Query is valid if it has at least 'EMPRESTA' and 'DE'
    invalid = query is None or query == '' or \
            'EMPRESTA ' not in query or ' DE ' not in query
    if invalid:
        raise ValueError('Invalid raw query: {0}'.format(query))
    # Return True if valid
    return True


@hpr.log_method(TESTING)
@hpr.timing
def raw_query(query_str, tbs):
    # Takes in raw query string and process the raw query to do singular
    # valid queries. E.g. breaks down query1 UNETELO CN query2 into 2 separate
    # queries before unioning them afterwards
    # Check and strip ';'
    if query_str.strip()[-1] != ';':
        raise hpr.InvalidQueryError('Incomplete query missing ";"')
    # Check overall query
    check_query(query_str)
    # strip the ';' for queries
    query_str = query_str.strip(';')
    if query_str[0] == '(':
        # There are joins
        queries = re.split(r'\sUNETELO CN\s'
                           r'|\sUNETELO TODO CN\s'
                           r'|\sCOMUN CN\s'
                           r'|\sSACALE\s', query_str)
        joins = re.findall(r'\sUNETELO CN\s'
                           r'|\sUNETELO TODO CN\s'
                           r'|\sCOMUN CN\s'
                           r'|\sSACALE\s', query_str)
        # Sending in substring of atomic query to take away the outer brackets
        results = (atomic_query(q[1:-1], tbs)
                   for q in queries if check_query(q))
        result_tb, col_order = join_query_res(results, joins)
        return man.cols_to_rows(result_tb, ['TODO'])
    else:
        # Only one expression to evaluate
        result_tb, col_order = atomic_query(query_str, tbs)
        return man.cols_to_rows(result_tb, col_order)


@hpr.log_method(TESTING)
def join_query_res(results, joins):
    '''
    Join the query results according to the joins
    :param results: a list of query results (result_tb, col_order)
    :param joins: a list of join keywords
    :return: a single joined tb {col_names: [entries]}
    '''
    def join(res1, res2):
        conn = joins.pop(0)
        tb1 = res1[0]
        col_order_1 = res1[1]
        tb2 = res2[0]
        col_order_2 = res2[1]
        if conn == ' UNETELO CN ':
            return man.unite_tables(tb1, tb2, col_order_1, col_order_2, False)
        elif conn == ' UNETELO TODO CN ':
            return man.unite_tables(tb1, tb2, col_order_1, col_order_2, True)
        elif conn == ' COMUN CN ':
            return man.intersect_tables(tb1, tb2, col_order_1, col_order_2)
        elif conn == ' SACALE ':
            return man.left_outer_intersect(tb1, tb2, col_order_1, col_order_2)
        else:
            raise ValueError('Do not recognize connective')
    joined_res = fct.reduce(join, results)
    return joined_res


@hpr.log_method(TESTING)
def atomic_query(query_str, tables):
    '''
    Does an atomic query using the provided tables
    :param query_str: an atomic query is a valid query with one EMPRESTA and DE
    :param tables: a dict of tb_name (keys): tables (values). Each table is a
                dict of col_names (keys): col_entries (values)
    :return: table (a dict), col_order (a list of col_names for printing)
    '''
    '''
    if 'EMPRESTA pokemon_id DE pokemon' in query_str:
        print(query_str)
    '''
    # Get list of intervals (start, end) to mark the start and end of sub-exprns
    intervals = get_exprn_intervals(query_str)
    # Get and label the sub-expressions: "keyword + [variables]"
    sub_exprns = [query_str[itv[0]: itv[1]] for itv in intervals]
    l_sub_exprns = label_exprns(sub_exprns)
    '''
    print('\nFor query: {0}'.format(query_str))
    for label, exprn in l_sub_exprns.items():
        print('{0}: {1}'.format(label, exprn))
    '''
    # Get the queried table names and columns
    tnames = de(l_sub_exprns[' DE '])
    cols, col_funcs = emp(l_sub_exprns['EMPRESTA '])
    # Get the queried tables
    tb_list = [tables.get(tname) for tname in tnames]
    # Get the conditional subexpression if exists
    onde = l_sub_exprns.get(' ONDE ', None)
    if onde:
        # eval_onde returns a dict {tname: table}
        filtered_tbs = eval_onde(onde.replace('ONDE', '', 1).strip(), tables)
        # Filter the tables by the conditions
        tb_list = [filtered_tbs[tname] for tname in tnames]
    # Finish off with executing EMPRESTA ... DE ...
    # Do the string strip() here so that there won't be a case of ONDE being
    # misinterpreted as DE
    order = l_sub_exprns.get(' ORDENATELOS X ')
    if order is not None:
        # Order the tables if there is ORDENATELOS X
        tb_list = order_cols(order.replace(' ORDENATELOS X ', ''),
                             tb_list)
    # AGRUPATELOS
    grp_line = l_sub_exprns.get(' AGRUPATELOS X ')
    # TENIENDO
    grp_fil_line = l_sub_exprns.get(' TENIENDO ')
    # Add on the columns need for TENIENDO and AGRUPATELOS if they are not in
    # the column list
    new_cols = cols.copy()
    if grp_line:
        grp_col = grp_line.replace(' AGRUPATELOS X ', '').strip()
        if grp_col not in new_cols:
            new_cols.append(grp_col)
    if grp_fil_line:
        # split the line into var1, operator, var2
        var1, oper, var2 = split_clauses(grp_fil_line.replace(' TENIENDO ', '')
                                         .strip('() '))
        if '(' in var1:
            col_str = var1
        else:
            col_str = var2
        # Assumes the var1 will be a function with column name
        # Get the list of function names
        func_keys = list(eva.FUNC.keys())
        col_str, __ = [(strip_func(col_str), func) for func in func_keys
                       if func + '(' in col_str][0]
        if col_str not in new_cols:
            # Add the col if it is not in the list of columns
            new_cols.append(col_str)
    # Table list is reduced to a single table with all the columns stated in the
    # cols (list)
    result_tb = emp_de_two(tb_list, new_cols, col_funcs)
    # Get groupings if grouping is not None
    grouping = None
    if grp_line:
        grouping = get_grouping(grp_line.replace(' AGRUPATELOS X ', '').strip(),
                                result_tb)
        if grp_fil_line:
            # If there is a filter group condition, filter grouping
            grouping = filter_grps(grp_fil_line.replace(' TENIENDO ', '')
                                   .strip('() '), result_tb, grouping)
    # Remove columns added for AGRUPATELOS and TENIENDO
    result_tb = man.reduce_tb(result_tb, cols)
    # Do the column functions on the result table
    # result_tb = do_col_funcs(result_tb, col_funcs)
    result_tb = do_col_funcs_two(result_tb, col_funcs, grouping)
    # return result table and the cols order of the query
    # If DIVERGENTE is true, remove duplicates
    if col_funcs['DIVERGENTE']:
        result_tb = man.rmv_dups(result_tb)

    # Check for SOLO expression, if there is cut_off the rows
    solo = l_sub_exprns.get(' SOLO ')
    if solo is not None:
        # Cut off rows
        result_tb = cutoff_rows(solo.strip(' SOLO '), result_tb)
    return result_tb, cols


@hpr.log_method(TESTING)
def unite_tables(evals):
    '''
    :param evals: a list of dicts with col_name (key) col_entries (value)
    :return: union all the rows of all the columns in all the evaluations
    '''
    all_entries = [entries for tb in evals for cname, entries in tb.items()]
    return fct.reduce(lambda col1, col2: col1 + col2, all_entries)


@hpr.log_method(TESTING)
def get_exprn_intervals(exprn):
    # Get the starting indexes of the keywords in the expression + last index
    indexes = [exprn.index(kw) for kw in KWS if kw in exprn] + [len(exprn)]
    # Join the indexes to make intervals (start, end) that marks the start and
    # end of expressions
    intervals = [(indexes[i], indexes[i + 1]) for i in range(len(indexes))
                 if i < len(indexes) - 1]
    return intervals


@hpr.log_method(TESTING)
def label_exprns(exprns):
    # Label expressions by keywords
    lst = [{kw: exprn} for exprn in exprns for kw in KWS if kw in exprn]

    def add_exprn(labeled, exprn):
        labeled_keys = list(labeled.keys())
        exprn_keys = list(exprn.keys())
        if exprn_keys[0] not in labeled_keys:
            labeled.update(exprn)
        return labeled

    return fct.reduce(add_exprn, lst)
    # return {kw: exprn for exprn in exprns for kw in KWS if kw in exprn}


@hpr.log_method(TESTING)
def emp(line):
    if line:
        line = line.replace('EMPRESTA ', '', 1)
        # Default is without DIVERGENTE
        funcs = {'DIVERGENTE': False}
        if 'DIVERGENTE' in line:
            funcs['DIVERGENTE'] = True
            line = line.replace('DIVERGENTE ', '', 1).strip()
        # Split the line into cols and check for column functions
        raw_cols = line.split(',')
        func_keys = list(eva.FUNC.keys())

        funcs.update({strip_func(col): func
                     for col in raw_cols for func in func_keys
                      if func + '(' in col})
        cols = list(map(lambda col: clean_col(col), raw_cols))
        return cols, funcs


def strip_func(col):
    '''
    Remove the function attached to a column name, i.e. FUNC(col_name), return
    col_name
    :param col: string
    :return: column name string
    '''
    __, col = col.split('(')
    return col.strip(')').strip()


def clean_col(col):
    '''
    Given a column name which might have a function attached return only
    the column name
    :param col: column name string
    :return: column name
    '''
    if '(' in col and ')' in col:
        return strip_func(col)
    else:
        return col.strip()


@hpr.log_method(TESTING)
def de(line):
    if line:
        tbs = line.replace('DE ', '').strip().split(',')
        return [tb.strip() for tb in tbs]


@hpr.log_method(TESTING)
def emp_de_two(tables, cols, col_funcs):
    '''
    Reduce a list of tables to a single table that have
    the required cols in the list
    :param tables: a list of dicts with col_name (key) and entries (value)
    :param cols: a list of col_names
    :param col_funcs: functions to executes on column entries, a dict
    :return: a single dict with col_name (key) and entries (value)
    '''
    # reduce each table of the list
    reduced = [man.reduce_tb(tb, cols) for tb in tables]
    '''
    def check_tb(table):
        return {col_name: perf_func(col_name, entries)
                for col_name, entries in table.items()}

    def perf_func(col_name, entries):
        if col_funcs.get(col_name, None) is None:
            # if there's no need to perform col func, return entries as it is
            return entries
        # Get the name of the column function
        func_name = col_funcs[col_name]
        # perform col functions on column entries
        return [eva.FUNC[func_name](entries)]

    reduced = [check_tb(tb) for tb in reduced]
    '''
    # Join all the tables together into one
    joined = man.combine(reduced)
    return joined


@hpr.log_method(TESTING)
def do_col_funcs(table, col_funcs):
    '''
    Given a dict of column functions mapped to column names, perform them on
    column entries
    :param table: a dict {col_name: [entries]}
    :param col_funcs: a dict {col_name: func_name}
    :return: a table {col_name: [entries]}
    '''
    def perf_func(col_name, entries):
        if col_funcs.get(col_name, None) is None:
            # if there's no need to perform col func, return entries as it is
            return entries
        # Get the name of the column function
        func_name = col_funcs[col_name]
        # perform col functions on column entries
        return [eva.FUNC[func_name](entries)]

    return {col_name: perf_func(col_name, entries)
            for col_name, entries in table.items()}


@hpr.log_method(TESTING)
def perf_func(col_name, entries, col_funcs, grouping=None):
    '''
    Given a dictionary of column functions mapping to column name, perform
    column function on column entries. Do it by groups if there is grouping
    :param col_name: string column name
    :param entries: a list of values
    :param col_funcs: a dict {col_name: func_name}
    :param grouping: a list of [indexes], each sublist is a equivalence class
    :return: a list of entries [val1, val2...]
    '''
    if grouping:
        # there are grouping
        if col_funcs.get(col_name):
            func_name = col_funcs[col_name]
            # Perform column function on each grouping of the entries
            perf_entries = [eva.FUNC[func_name](man.get_entries(entries, grp))
                            for grp in grouping]
        else:
            # No column function, return the first element of each group
            perf_entries = [entries[grp[0]] for grp in grouping]
    else:
        # There are no grouping
        if col_funcs.get(col_name):
            # There is column function for the column
            # Get the name of the column function
            func_name = col_funcs[col_name]
            # perform col functions on column entries
            perf_entries = [eva.FUNC[func_name](entries)]
        else:
            # if there's no need to perform col func, return entries as it is
            perf_entries = entries
    return perf_entries


@hpr.log_method(TESTING)
def do_col_funcs_two(tb, col_funcs, grouping=None):
    '''
    Given a dict of column functions mapped to column names, perform them on
    column entries partitioned by groups in grouping
    :param table: a dict {col_name: [entries]}
    :param col_funcs: a dict {col_name: func_name}
    :param grouping: a list of [indexes], each sublist is an equivalence class
    :return: a table {col_name: [entries]}
    '''
    return {col_name: perf_func(col_name, entries, col_funcs, grouping)
            for col_name, entries in tb.items()}


@hpr.log_method(TESTING)
def get_grouping(line, tb):
    '''
    Create a quotient set of all the row indexes of the table. Each equivalence
    class is a list of row indexes that are equivalent by the grouping of the
    line. e.g. GROUP age -> [[1, 2, 3], [4, 7, 9]] where row 1, 2, and 3 have
    age 10, and row 4, 7, 9 have age 20
    :param line: AGRUPATELOS X ..., but without the keyword so it would just be
                 the column name of the grouping
    :param tb: a dict {col_name: [entries]}
    :return: a grouping list [[row indexes], [row indexes]]
    '''
    # Get the column entries
    entries = tb.get(line.strip())
    if entries is None:
        # table does not have the column, invalid query
        raise hpr.InvalidQueryError('Cannot find {0} in table for grouping'
                                    .format(line))
    # Use defaultdict to create the quotient set

    def add_entry(dic, entry):
            # Add entry to default dict
            # entry is a tuple (index, entry_value)
            dic[entry[1]].append(entry[0])
            return dic
    # enumerate the entries to get the row indexes
    dic = fct.reduce(add_entry, enumerate(entries), col.defaultdict(list))
    # return the values of the defaultdict
    return list(dic.values())


@hpr.log_method(TESTING)
def filter_grps(line, tb, grouping):
    '''
    Filter out groups that do not meet filter condition before performing
    column functions on groups in do_col_func_two
    :param line: a TENIENDO condition without ' TENIENDO ' and '()'
    :param tb: a dict {col_name: [entries]}
    :param grouping: a list of [indexes], each sublist is an equivalence class
    :return: a list of [indexes], each equivalence class meets the condition
    '''
    # split the line into var1, operator, var2
    var1, oper, var2 = split_clauses(line)
    if '(' in var1:
        col_str = var1
        val_str = var2
    else:
        col_str = var2
        val_str = var1
    # Get the list of function names
    func_keys = list(eva.FUNC.keys())
    col, func = [(strip_func(col_str), func) for func in func_keys
                 if func + '(' in col_str][0]
    if tb.get(col) is None:
        raise hpr.InvalidQueryError('Table do not have column: {0}'.format(col))
    # Get the list of entry values of each group after performing function
    values = [eva.FUNC[func](man.get_entries(tb[col], grp)) for grp in grouping]
    # Filter list of values by the var2 using operator, return a list of group
    # ids of groups that passed filter condition
    if col_str == var1:
        filtered_grps = [grp_id for grp_id, val in enumerate(values)
                         if eva.OPER[oper](var1=val,
                                           var2=hpr.parse_val(val_str))]
    else:
        filtered_grps = [grp_id for grp_id, val in enumerate(values)
                         if eva.OPER[oper](var1=hpr.parse_val(val_str),
                                           var2=val)]
    return [grouping[i] for i in filtered_grps]


@hpr.log_method(TESTING)
def order_cols(line, table_list):
    '''
    Execute 'ORDENATELOS X' command
    :param line: line without the 'ORDENATELOS X'
    :param table_list: a dict {col_name: [entries]}
    :return: a dict {col_name: [entries]}
    '''

    def read_line(l):
        col_name, dir_str = l.split(' PA ')
        if 'RIBA' in dir_str:
            # Sort ascending
            asc = True
        elif 'BAJO' in dir_str:
            # Sort descending
            asc = False
        else:
            raise ValueError('direction string: {0}'.format(dir_str))
        return col_name.strip(), asc
    col_name, asc = read_line(line)
    # Get table using col_name
    table = [tb for tb in table_list if man.has_col(tb, col_name)][0]
    # Get the list of sorted entry indexes for col_name
    index = man.get_sorted_indexes(table[col_name], asc)
    ordered_tb = {col_name: man.order_col(entries, index)
                  for col_name, entries in table.items()}
    tb_list = [tb for tb in table_list if not man.has_col(tb, col_name)]
    tb_list.append(ordered_tb)
    return tb_list


@hpr.log_method(TESTING)
def cutoff_rows(line, table):
    '''
    Cut off all the columns of the table by the required number of entries
    :param line: line without 'SOLO'
    :param table: a dict {col_name: [entries]}
    :return:
    '''
    try:
        num_of_rows = int(line.strip())
    except (TypeError, ValueError):
        # Raise exception if cannot parse line as int, since something is wrong
        raise hpr.InvalidQueryError('Type error at SOLO expression')
    return {col_name: entries[:num_of_rows]
            for col_name, entries in table.items()}


@hpr.log_method(TESTING)
def eval_onde(line, tables):
    '''
    Evaluate a ONDE query
    :param line: ONDE query without the 'ONDE ' keyword
    :param tables: a dict {tname: tb}
    :return: a dict {tname: filtered_tb}
    '''
    # Get atomic conditional statement and connectives from line
    atomics, conn = man.split_exprn(line)
    # all the filtered indexes from each condition statement
    f_cols_lst = [eval_cond(cond, tables) for cond in atomics]
    # Reduce the list of dicts to one single dict by joining them together
    # by the connectives
    join = lambda ind1, ind2: man.join_filt_indexes(tables.keys(),
                                                    ind1, ind2, conn.pop(0))
    f_cols = fct.reduce(join, f_cols_lst)
    if not isinstance(f_cols, bool):
        # If ONDE consists of only an EXISTE(...) clause then there is no need
        # to filter tables
        return man.filter_tables(tables, f_cols)
    elif f_cols:
        # f_cols is a boolean value, i.e. a single EXISTE(...) clause, return
        # tables if it is True, else raise TerminateQueryError
        return tables
    elif not f_cols:
        raise hpr.TerminateQueryError('Existe condition is False')
    else:
        raise hpr.InvalidQueryError('Something is wrong with the query')


@hpr.log_method(TESTING)
@hpr.timing
def eval_cond(cond, tables):
    '''
    Evaluates a single condition then returns a dict of the filtered indexes of
    columns involved in the condition
    :param cond: a single conditional expression
    :param tables: a dict of tables {tname: tb}
    :return: a dict {col_name: [index that fulfills condition]}
    '''
    if ' EN ' in cond:
        col_name, inner_query = cond.split(' EN ', 1)
        # On filter column by inner query result
        tname, tb = [(tname, tb) for tname, tb in tables.items()
                     if man.has_col(tb, col_name)][0]
        col_entries = tb[col_name]
        return filter_by_query(tname, col_name,
                               # inner query take away the brackets
                               col_entries, inner_query[1:-1], tables)
    if 'EXISTE ' in cond:
        inner_query = cond.replace('EXISTE (', '', 1)[:-1]
        if not exist_condition(inner_query, tables):
            # if return False, terminate the current query, otherwise continue
            raise hpr.TerminateQueryError()
        else:
            return True
    clauses = split_clauses(cond)
    var1, oper, var2 = clauses
    if oper == 'ENTRE':
        # filter by range
        # Get table, assumes unique column name
        tname, tb = [(tname, tb) for tname, tb in tables.items()
                     if man.has_col(tb, var1)][0]
        col_entries = tb[var1]
        start, end = var2.strip(' (').strip(') ').split(' Y ')
        return filter_by_range(tname, col_entries, int(start), int(end))
    else:
        if man.is_col(tables, var1) and man.is_col(tables, var2):
            # filter by cols
            tname1, tb1 = [(tname, tb) for tname, tb in tables.items()
                           if man.has_col(tb, var1)][0]
            tname2, tb2 = [(tname, tb) for tname, tb in tables.items()
                           if man.has_col(tb, var2)][0]
            col_entries1 = tb1[var1]
            col_entries2 = tb2[var2]
            return filter_by_col(tname1, col_entries1, tname2, col_entries2)
        elif man.is_col(tables, var1):
            # filter by val
            # Get table, assumes unique column name
            tname, tb = [(tname, tb) for tname, tb in tables.items()
                         if man.has_col(tb, var1)][0]
            col_entries = tb[var1]
            return filter_by_val(tname, col_entries, oper, hpr.parse_val(var2))
        else:
            # Get table, assumes unique column name
            tname, tb = [(tname, tb) for tname, tb in tables.items()
                         if man.has_col(tb, var2)][0]
            col_entries = tb[var2]
            return filter_by_val(tname, col_entries, oper, hpr.parse_val(var1))


@hpr.log_method(TESTING)
def filter_by_val(tname, col_entries, oper, val):
    '''
    Filter column by the stated value
    :param tname: table name
    :param col_entries: column entries
    :param oper: operator to for comparison
    :param val: value which can be a string, int or float
    :return: a dict {col_name: a list of col indexes}
    '''
    # Filter column and return indexes
    filtered = [index for index, entry in enumerate(col_entries)
                if eva.OPER[oper](var1=entry, var2=val)]
    return {tname: filtered}


@hpr.log_method(TESTING)
def filter_by_val_list(tname, col_entries, vals):
    '''
    Filter column by a list of values
    :param tname: table name
    :param col_entries: column entries
    :param vals: a list of values to check
    :return: a dict {col_name: a list of col indexes with value in vals
    '''
    filtered = [index for index, entry in enumerate(col_entries)
                if entry in vals]
    return {tname: filtered}


@hpr.log_method(TESTING)
def filter_by_col(tname1, col1_entries, tname2, col2_entries):
    '''
    Filter two columns by matching the two with each other
    :param tname1: table name 1
    :param col1_entries: column1 entries
    :param tname2: table name 2
    :param col2_entries: column2 entries
    :return: a dict {col1_name: a list of col indexes, col2_name: index list}
    '''
    filtered = dict()
    # Filter col1 entries
    filtered.update(filter_by_val_list(tname1, col1_entries, col2_entries))
    # Filter col2 entries
    filtered.update(filter_by_val_list(tname2, col2_entries, col1_entries))
    return filtered


@hpr.log_method(TESTING)
def filter_by_range(tname, col_entries, start, end):
    '''
    Filter column values if they exists with the start and end
    :param tname: table name
    :param col_entries: column entries
    :param start: the starting value of the range
    :param end: the ending value of the range
    :return: a dict {col_name: a list of col indexes}
    '''
    filtered = [index for index, entry in enumerate(col_entries)
                if eva.betw(entry, start, end)]
    return {tname: filtered}


@hpr.log_method(TESTING)
def filter_by_query(tname, col_name, col_entries, query, tables):
    '''
    Make an inner query and filter col_entries on the results of the query
    :param tname: tname
    :param col_name: column name
    :param col_entries: column entries
    :param query: inner query
    :param tables: dict{tname: tables}
    :return: a dict {col_name: [col indexes]}
    '''
    result_tb, col_order = atomic_query(query, tables)
    if result_tb.get(col_name, None) is None:
        raise hpr.InvalidQueryError(query)
    # Need to convert generator to a list
    result_entries = result_tb[col_name]
    return filter_by_val_list(tname, col_entries, list(result_entries))


@hpr.log_method(TESTING)
def exist_condition(cond, tables):
    '''
    ONDE condition on EXISTE(query), only continue with query if EXISTE return
    True, return true if condition returns at least one row
    :param cond: condition
    :param tables: dict{tname: tables}
    :return: bool value
    '''
    result_tb, col_order = atomic_query(cond, tables)
    return len(list(result_tb.keys())) > 0


@hpr.log_method(TESTING)
def split_clauses(cond):
    # Splits the atomic condition line into VAR1, OPERATOR, VAR2
    operators = [op for op in eva.OPER.keys() if op in cond]

    def get_key(x): return len(x)
    # Use the operator with the max length since '<=' can be read as '<' or '='
    clauses = cond.split(max(operators, key=get_key))
    return clauses[0].strip(), max(operators, key=get_key), clauses[1].strip()


if __name__ == '__main__':
    # Testing split clauses
    cond = 'RUT = Comprador'
    cl1, op, cl2 = split_clauses(cond)
    print('{0} {1} {2}'.format(cl1, op, cl2))
    cond1 = 'Cervezas.nombre PARECIO A "Cristal"'
    cl11, op1, cl12 = split_clauses(cond1)
    print('VAR1: {0}, COND: {1}, VAR2: {2}'.format(cl11, op1, cl12))
