from collections import namedtuple
import manipulation as man
import helper as hpr

# ------------------------TESTING PURPOSE------------------------------------- #
# Toggle TESTING to log methods
TESTING = False

# ---------------------------------------------------------------------------- #


def read_csv(fname, file):
    '''
    :param fname: filename
    :param file: csv file
    :return: a dictionary with name: table name and entries: list of entries
    '''
    # use filename as the namedtuple name
    name = fname.replace('.csv', '')
    # first line in file has the attribute names and types
    frst = file.readline().strip()
    line = frst.split(',')
    cols = [a.split(':')[0] for a in line]
    # Get the types using the type strings
    types = get_types([a.split(':')[1] for a in line])
    # Create the namedtuple item using the name and cols
    item = namedtuple(name, cols)
    entries = read_entries(file, item, types)
    return {'name': name, 'entries': entries}


def read_table(fname):
    '''
    :param fname: filename
    :return: a dictionary with table name and each column as sep key-val pairs
    '''
    file = open(fname, 'r')
    # use filename as the namedtuple name
    name = fname.replace('.csv', '')
    # first line in file has the attribute names and types
    frst = file.readline().strip()
    line = frst.split(',')
    cols = [a.split(':')[0] for a in line]
    # Get the types using the type strings
    types = get_types([a.split(':')[1] for a in line])
    col_entries = read_entries_two(file, types)
    # print('Column entries: {0}'.format(col_entries))
    hpr.log(TESTING, '{0} has {1} entries'.format(name, len(col_entries[0])))
    # Column entries zipped with column names
    named_col_entries = zip(cols, col_entries)
    table = dict(named_col_entries)
    # Close file
    file.close()
    return name, table


def read_entries(file, item, types):
    '''
    :param file: the file without the first line
    :param item: namedtuple representing the item
    :param types: the types of the columns
    :return: a list of entries (which are named tuples)
    '''
    return [read_line(item, types, line.strip()) for line in file]


def read_entries_two(file, types):
    '''
    :param file: the file without the first line
    :param types: the types of the columns
    :return: a list of columns entries
    '''
    entries = [read_line_two(types, line.strip()) for line in file]
    cols = list(zip(*entries))
    return cols


def read_line(item, types, line):
    '''
    :param item: a namedtuple to be instantiated
    :param types: the data type of each column in the line
    :param line: a list of casted data
    :return: instantiated namedtuple item
    '''
    col_data = line.split(',')

    def cast(data, type):
        if data != '':
            return type(data)
        else:
            # Return None if there's no data
            return None

    return item._make(map(lambda data, type: cast(data, type), col_data, types))


def read_line_two(types, line):
    '''
    :param types: the data type of each column in the line
    :param line: a list of casted data
    :return: a list of entry column values
    '''
    col_data = line.split(',')
    def cast(data, type):
        if data != '':
            return type(data)
        else:
            # Return None if there's no data
            return None

    return list(map(lambda data, type: cast(data, type), col_data, types))


def get_types(lst):
    '''
    :param lst: a list of strings types, e.g. ['int', 'str']
    :return: list of types
    '''
    types = {'int': int, 'str': str, 'string': str, 'float': float}
    return [types.get(t) for t in lst]


def query_entries(table, cols, start=0, end=None):
    '''
    :param table: table to query
    :param cols: list of column names
    :param start: starting row
    :param end: ending row + 1
    :return: row entries of selected cols from table from start to stop
    '''
    # Get the rows from the selected columns of the table
    # Check that cols are in table, raise error if not
    if not man.has_all_cols(table, cols):
        raise ValueError('Column not in table')
    queried = [table.get(col)[start: end] for col in cols]
    # zip the columns together as rows
    rows = list(zip(*queried))
    return rows


if __name__ == '__main__':
    # Using namedtuples
    # Read the file personas.csv
    pers = read_csv('personas.csv', open('personas.csv', 'r'))
    print('Table {0} has {1} entries.'
          .format(pers['name'], len(pers['entries'])))
    # print sample entry
    print(*[entry for entry in pers['entries'][:3]], sep='\n')

    # Read the file comunas.csv
    cons = read_csv('comunas.csv', open('comunas.csv', 'r'))
    print('\nTable {0} has {1} entries.'
          .format(cons['name'], len(cons['entries'])))
    # print sample entry
    print(*[entry for entry in cons['entries'][:3]], sep='\n')

    # Read the file viajes.csv
    vias = read_csv('viajes.csv', open('viajes.csv', 'r'))
    print('\nTable {0} has {1} entries.'
          .format(vias['name'], len(vias['entries'])))
    # print sample entry
    print(*[entry for entry in vias['entries'][109812:109815]], sep='\n')

    # Read the file personas.csv
    name, tb = read_table('personas.csv')
    print('\nTable {0} has {1} entries.'
          .format(name, len(tb['Persona'])))
    # print sample entry
    print(*query_entries(tb, ['Persona', 'AnoNac', 'Sexo'], end=3), sep='\n')