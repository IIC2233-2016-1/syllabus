import functools as fct
import helper as hpr
import re
import collections as col

# ------------------------TESTING PURPOSE------------------------------------- #
# Toggle TESTING to log methods
TESTING = False

# ---------------------------------------------------------------------------- #


@hpr.log_method(TESTING)
def printable(rows):
    # return a printable string format of rows
    #  col1 | col2
    row_s = (' | '.join([str(val) for val in row if val != '']) for row in rows)
    return '\n'.join(row_s)


@hpr.log_method(TESTING)
def cols_to_rows(cols_dict, col_order):
    # convert {'col_name': [entry1,...], 'col_name': [entry1,...]} to rows
    if 'TODO' in col_order:
        # Just all columns without order
        ordered_cols = (col for col_name, col in cols_dict.items())
    else:
        ordered_cols = (cols_dict[col] for col in col_order)
    # return list(zip(*cols_dict.values()))
    return list(zip(*ordered_cols))


@hpr.log_method(TESTING)
def rows_to_tb(rows, col_names):
    '''
    Convert a list of rows (tuples) into a a table
    :param rows: a list of tuples
    :param col_names: a list of column names
    :return: a dict {col_name: [entries]}
    '''
    # Unzip rows to cols
    col_entries = list(zip(*rows))
    # Check the number of cols and col names matches, add arbitrary if do not
    if len(col_names) != len(col_entries):
        col_n_size = len(col_names)
        col_e_size = len(col_entries)
        dif = col_n_size - col_e_size
        col_names += ['col{0}'.format(i + col_n_size)
                      for i in range(0, abs(dif))]
    # Make a list of dictionaries putting col_names with entries
    col_lst = list(map(lambda c_name, col: {c_name: list(col)},
                       col_names, col_entries))

    def join_cols(col1, col2):
        col1.update(col2)
        return col1
    tb = fct.reduce(join_cols, col_lst)
    return tb


def duplicate(entries, new_size):
    '''
    :param entries: a list of row entries of a single column
    :param new_size: new list size to fit into
    :return: a list in which each entry is duplicated by x times
    '''
    repeat = int(new_size / len(entries))
    return [entry for entry in entries for __ in range(0, repeat)]


def combined_size(tables):
    '''
    :param tables: a list of dicts {col_names (key): col_entries (value)}
    :return: the size of the combined tables
    '''
    tb_sizes = (len(list(tb.values())[0]) for tb in tables
                if len(tb.values()) > 0)
    return fct.reduce(lambda a, b: a * b, tb_sizes, 1)


def is_col(tables, string):
    '''
    :param tables: a dict {tb_name: tbs}
    :param string: column name
    :return: bool on whether string is a column
    '''
    all_tbs = [tb for tname, tb in tables.items()]
    all_cols = [col_name for tb in all_tbs
                for col_name, col_entries in tb.items()]
    return string in all_cols


def has_col(table, col):
    return col != 'tb_nam' and col in table.keys()


def has_all_cols(table, cols):
    # Return bool on whether table has all the columns
    return all(has_col(table, col) for col in cols)


def get_cols(table, cols):
    # Return the columns that belong to the table
    if len(cols) == 1 and cols[0] == 'TODO':
        return table.keys()
    return list(filter(lambda c: has_col(table, c), cols))


@hpr.log_method(TESTING)
def combine(tables):
    '''
    :param tables: a list of dicts {col_names (key): col_entries (value)}
    :return: a dict of combined columns
    '''
    new_size = combined_size(tables)
    combined = {col_name: duplicate(entries, new_size)
                for tb in tables
                for col_name, entries in tb.items()}
    return combined


@hpr.log_method(TESTING)
def filter_col(table, col, func):
    # Returns a list of indexes of col entries that is true on the function
    hpr.log(TESTING, 'filter_col table keys: {0}'.format(table.keys()))
    if not has_col(table, col):
        raise ValueError('Column {0} not in table'.format(col))
    entries = table[col]
    return [i for i in range(len(entries)) if func(entries[i])]


def reduce_tb(table, cols):
    '''
    Reduce the table by only including the selected columns
    :param table: dictionary with col_name (key) and entries (value)
    :param cols: a list of col_names
    :return: a reduced table
    '''
    if len(cols) == 1 and cols[0] == 'TODO':
        # All columns of the table are required
        return table
    else:
        return {col: table[col] for col in cols if has_col(table, col)}


def split_exprn(exprn):
    '''
    Split expression by brackets into a list of atomic exprns and connectives
    :param exprn: a string which is the expression
    :return: an ordered list of atomic expressions and connectives
    '''
    atomics = re.split(r'\)\sY\s\(|\)\sO\s\(', exprn)
    connectives = re.findall(r'\)\sY\s\(|\)\sO\s\(', exprn)
    connectives = [conn[1:-1] for conn in connectives]
    return list(map(lambda x: clean_exprn(x), atomics)), connectives


def clean_exprn(exprn):
    '''
    Given an expression string, remove all unnecessary brackets
    :param exprn:
    :return: cleaned expression
    '''
    exprn = exprn.strip()
    # First strip lefthand side of '('
    left_stripped = exprn.lstrip('(')
    # Count number of '(' within expression
    inner_bracks = len(list(filter(lambda x: x == '(', left_stripped)))
    return left_stripped.strip(')') + (')' * inner_bracks)


def join_filt_indexes(tnames, index1, index2, connective):
    '''
    Join two indexes together based on table names and connective
    :param tnames: a list of table names used to retrieve filtered index list
                   from index1 and index2
    :param index1: a dict {tname: [filtered_indexes]}
    :param index2: a dict {tname: [filtered_indexes]}
    :param connective: a connective either Y o O
    :return: a joined dict {tname: [filtered_indexes]}
    '''
    if isinstance(index1, bool):
        return index2
    elif isinstance(index2, bool):
        return index1

    def join(lst1, lst2, conn):
        if lst1 is None:
            return lst2
        elif lst2 is None:
            return lst1
        else:
            if conn == ' Y ':
                return list(set(lst1).intersection(set(lst2)))
            elif conn == ' O ':
                return list(set(lst1).union(set(lst2)))
            else:
                raise ValueError('Unmatch connective: {0}'.format(conn))

    return {tname: join(index1.get(tname), index2.get(tname), connective)
            for tname in tnames
            if index1.get(tname, None) is not None or
            index2.get(tname, None) is not None}


@hpr.log_method(TESTING)
def get_entries(entries, indexes):
    # Get the entries at specific index of indexes
    entries = list(entries)
    return [entries[i] for i in indexes]


@hpr.log_method(TESTING)
def filter_table(table, indxs):
    '''
    for col_name, col_entries in table.items():
        if len(list(col_entries)) == 0:
            print('Column {0} is empty'.format(col_name))
    '''
    if indxs is None or len(indxs) == 0:
        # If the table does not need filtering return it immediately
        return table
    else:
        return {col_name: get_entries(col_entries, indxs)
                for col_name, col_entries in table.items()}


@hpr.log_method(TESTING)
def filter_tables(tables, indexes):
    '''
    Filter tables by the column indexes
    :param tables: a dict {tname: table}
    :param indexes: a dict {tname: [filtered_indexes]}
    :return: a dict {tname: table}
    '''
    return {tname: filter_table(table, indexes.get(tname, None))
            for tname, table in tables.items()}


def get_dup_lst(col_entries, prev_lst=None):
    '''
    Get a list of equivalence classes in which each equivalence class has the
    indexes of column entries that have the same value
    :param col_entries: Column entries
    :param prev_lst: a previous list of equivalence class to build on. If there
                    is a previous list, only need to look up the indexes of the
                    list
    :return: a list of [index1, index2,..], where each sublist is an equivalence
             class
    '''
    # if prev_lst is not None, only need to look the corresponding entries in
    # the previous list, previous list have the indexes of duplicate entries
    # of other columns, therefore if it is not a duplicate entry in the other
    # col, the overall row will not be a duplicate
    def add_entry(dic, entry):
            # Add entry to default dict entry val (key) index (value)
            dic[entry[1]].append(entry[0])
            return dic

    def get_dups(entries):
            # each entry is a tuple (val: index)
            # Run through list and append the entry index of entries with
            # the same value to the same index list
            dic = fct.reduce(add_entry, entries, col.defaultdict(list))
            # Create a duplicate list with sublist of indexes of entries
            # with the same value, each sublist has >1 length,
            # i.e. each sublist is an equivalence class with cardinality > 1
            dup_lst = [lst for __, lst in dic.items() if len(lst) > 1]
            return dup_lst
    if prev_lst is not None:
        def get_entries(indexes):
            return [(index, col_entries[index]) for index in indexes]
        # Get the entry values for each sublist
        entries_lst = [get_entries(lst) for lst in prev_lst]
        # A list of lists of lists of equivalence classes
        dup_lst_lst = [get_dups(entries) for entries in entries_lst]
        # Reduce it to list of lists of equivalence classes
        dup_lst = fct.reduce(lambda a, b: a + b, dup_lst_lst)
        return dup_lst
    else:
        return get_dups(enumerate(col_entries))


@hpr.log_method(TESTING)
def rmv_dups(table):
    '''
    Remove all the duplicating rows
    :param table: a dict {col_name: [entries]}
    :return: a dict {col_name: [entries]}
    '''
    col_names = list(table.keys())
    # Get the duplicate list of the first column
    first_col_name = col_names.pop(0)
    first = list(table[first_col_name])
    # todo fix bug
    # A dirty fix of a bug, the entries is a generator and therefore making it
    # into a list above consumes it, need to re-add the entries list
    table[first_col_name] = first
    if len(first) == 0:
        print('Col: {0} has len 0'.format(first_col_name))
    tb_size = len(first)
    lst = get_dup_lst(first)

    def recur_dup(prev_lst, col_name):
        return get_dup_lst(table[col_name], prev_lst)
    dup_lst = fct.reduce(recur_dup, col_names, lst)
    # Each sublist is an equivalence class, reduce sublist to size 1
    # Reduce the whole list to having only the starting element of each sublist
    dup_lst = [lst[0] for lst in dup_lst]
    # Inverse the list to get the indexes of entries not to be removed
    filter_lst = [i for i in range(0, tb_size) if i not in dup_lst]
    return filter_table(table, filter_lst)


@hpr.log_method(TESTING)
def order_col(entries, index):
    '''
    Order entries by the list of index
    :param entries: a list of entries
    :param index: a list of column indexes
    :return: a list of ordered entries
    '''
    if len(entries) != len(index):
        raise ValueError('Entries length {0} != index length {1}'
                         .format(len(entries), len(index)))
    return [entries[i] for i in index]


@hpr.log_method(TESTING)
def get_sorted_indexes(entries, asc):
    '''
    Get the indexes of the sorted entries
    :param entries: column entries
    :param asc: boolean on sort ascending or descending
    :return: a list of indexes
    '''
    numbered = list(enumerate(entries))
    # Sort numbered list on its value
    if asc:
        sorted_lst = sorted(numbered, key=lambda x: x[1])
    else:
        sorted_lst = sorted(numbered, key=lambda x: x[1], reverse=True)
    return [index for index, val in sorted_lst]


def check_num_of_col(tb1, tb2):
    # Raise error if the column numbers do not match
    if len(list(tb1.keys())) != len(list(tb2.keys())):
        raise hpr.InvalidQueryError('Unmatching column numbers')


def check_type_match(type_lst1, type_lst2):
    # Raise error if there is mismatch of types
    if type_lst1 != type_lst2:
        raise hpr.InvalidQueryError('Unmatching column types')


def get_col_types(tb, col_order):
    # Return a list of column types following col_order
    # Assumes it will not be TODO
    if len(col_order) == 1 and col_order[0] == 'TODO':
        return [e[0].__class__ for __, e in tb.items() if len(e) > 0]
    else:
        return [tb[col_name][0].__class__ for col_name in col_order
                if len(tb[col_name]) > 0]


# Joining tables for UNETELO CN, COMUN CN
def unite_tables(tb1, tb2, col_order1, col_order2, repeat=False):
    '''
    Return a union of two tables, with repeatable rows toggleable
    :param tb1: a dict {col_name: [entries]}
    :param col_order1: list of column order
    :param tb2: a dict {col_name: [entries]}
    :param col_order2: list of column order
    :param repeat: boolean on whether duplicate rows are allowed
    :return: a list of rows
    '''
    # Check if the column number matches
    check_num_of_col(tb1, tb2)
    # Check column types matches
    check_type_match(get_col_types(tb1, col_order1),
                     get_col_types(tb2, col_order2))
    # Convert the two tables to rows and unite them
    tb1_rows = cols_to_rows(tb1, col_order1)
    tb2_rows = cols_to_rows(tb2, col_order2)
    if repeat:
        joined_rows = tb1_rows + tb2_rows
    else:
        tb1_rows_set = set(tb1_rows)
        tb2_rows_set = set(tb2_rows)
        # Using set removes duplicates
        combined = tb1_rows_set.union(tb2_rows_set)
        joined_rows = list(combined)
    # Convert rows back to a table {col_names: [entries]}
    if len(joined_rows) == 0:
        # No rows, return empty dict
        return {}, col_order1
    else:
        return rows_to_tb(joined_rows, col_order1), col_order1


def intersect_tables(tb1, tb2, col_order_1, col_order_2):
    '''
    Return an intersection of the two tables, i.e. rows that exists in both
    table 1 and table 2
    :param tb1: a dict {col_name: [entries]}
    :param col_order_1: list of column order
    :param tb2: a dict {col_name: [entries]}
    :param col_order_2: list of column order
    :return: a list of rows
    '''
    # Check if the column number matches
    check_num_of_col(tb1, tb2)
    # Check column types matches
    check_type_match(get_col_types(tb1, col_order_1),
                     get_col_types(tb2, col_order_2))
    # Convert the two tables to rows
    tb1_rows = cols_to_rows(tb1, col_order_1)
    tb2_rows = cols_to_rows(tb2, col_order_2)
    tb1_rows_set = set(tb1_rows)
    tb2_rows_set = set(tb2_rows)
    # Using set to get intersection
    joined_rows = list(tb1_rows_set.intersection(tb2_rows_set))
    # Convert rows back to a table {col_names: [entries]}
    if len(joined_rows) == 0:
        # No rows, return empty dict
        return {}, col_order_1
    else:
        return rows_to_tb(joined_rows, col_order_1), col_order_1


def left_outer_intersect(tb1, tb2, col_order1, col_order2):
    '''
    Return rows that are in table1 but not in table2
    :param tb1: a dict {col_name: [entries]}
    :param tb2: a dict {col_name: [entries]}
    :return: a list of rows
    '''
    # Check if the column number matches
    check_num_of_col(tb1, tb2)
    # Check column types matches
    check_type_match(get_col_types(tb1, col_order1),
                     get_col_types(tb2, col_order2))
    # Convert the two tables to rows
    tb1_rows = cols_to_rows(tb1, col_order1)
    tb2_rows = cols_to_rows(tb2, col_order2)
    tb1_rows_set = set(tb1_rows)
    tb2_rows_set = set(tb2_rows)
    # Get difference between tb1 and tb2
    left_outer = tb1_rows_set.difference(tb2_rows_set)
    joined_rows = list(left_outer)
    # Convert rows back to a table {col_names: [entries]}
    if len(joined_rows) == 0:
        # No rows, return empty dict
        return {}, col_order1
    else:
        return rows_to_tb(joined_rows, col_order1), col_order1

# -------------------------- Consult2 -----------------------------------------#


def get_col(col_name, tbs):
    return {col_name: tb[col_name] for tname, tb in tbs.items()
            if tb.get(col_name) is not None}
