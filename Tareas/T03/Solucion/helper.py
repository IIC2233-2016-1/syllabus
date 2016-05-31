import time


def log_method(testing):
    # Decorator to print methods if TESTING is True
    def _log_method(function):
        def __log_method(*args, **kwargs):
            if testing:
                print(function.__name__)
            return function(*args, **kwargs)
        return __log_method
    return _log_method


def log(testing, text):
    if testing:
        print(text)


def timing(f):
    # http://stackoverflow.com/questions/5478351/python-time-measure-function
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        #print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


def parse_val(val_string):
    # Convert val_string to str, float, or int
    if '"' in val_string:
        return val_string.strip('"')
    if "'" in val_string:
        return val_string.strip("'")
    elif '.' in val_string:
        return float(val_string)
    else:
        return int(val_string)


class TerminateQueryError(Exception):
    pass


class InvalidQueryError(Exception):
    def __init__(self, query):
        super().__init__('Invalid query:\n{0}'.format(query))
