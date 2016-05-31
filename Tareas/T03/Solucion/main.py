import helper as hpr
import consult as cns
import manipulation as man


# ------------------------TESTING PURPOSE------------------------------------- #
# Toggle TESTING to log methods
TESTING = False

# ---------------------------------------------------------------------------- #


def select_rows(rows, end, start=0):
    '''
    :param rows: a generator of rows
    :return a fixed number of rows
    '''
    rows = list(rows)
    size = len(rows)
    if size < (end - start):
        return rows
    return (rows[i] for i in range(start, end))


def proc_consult_file(consult_file, result_file):
    tbs, consults = cns.get_consults(consult_file)
    result_f = open(result_file, 'a')

    for i in range(len(consults)):
        c = consults[i]
        hpr.log(TESTING, 'At consult: {0}'.format(c))
        to_file = '------- CONSULTA {0} -------\n'.format(i + 1)
        try:
            to_file += man.printable(cns.raw_query(c, tbs))
        except ValueError as ve:
            print('Error: {0}'.format(ve))
            to_file += 'FALLIDA'
        except hpr.InvalidQueryError as iqe:
            print('Error: {0}'.format(iqe))
            to_file += 'FALLIDA'
        except hpr.TerminateQueryError as tqe:
            print('Query terminated: {0}'.format(tqe))
            # Append an empty line
            to_file += '\n'
        except Exception as e:
            print('Error: {0}'.format(e))
            to_file += 'FALLIDA'
        finally:
            print('Completed consult {0}.'.format(i + 1))

        print(to_file, end='\n', file=result_f)
        hpr.log(TESTING, '\nConsult {0}: {1}'.format(i + 1, c))
        hpr.log(TESTING, to_file)
    result_f.close()
    return tbs


def loop_consult(tbs, rows):
    in_loop = True

    while in_loop:
        query = input('\nPlease enter valid query:\n')
        if query:
            try:
                selected_rows = select_rows(cns.raw_query(query, tbs), rows)
                print(man.printable(selected_rows))
            except ValueError as ve:
                print('Error: {0}'.format(ve))
            except hpr.InvalidQueryError as iqe:
                print('Error: {0}'.format(iqe))
            except hpr.TerminateQueryError as tqe:
                print('\n')
            except Exception as e:
                print('Error: {0}'.format(e))
        else:
            in_loop = False


if __name__ == '__main__':
    consult_file = 'consultas.txt'
    result_file = 'resultados.txt'

    tbs = proc_consult_file(consult_file, result_file)

    rows = 15
    loop_consult(tbs, rows)
