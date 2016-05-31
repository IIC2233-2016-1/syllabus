

def lteq(var1, var2):
    return var1 <= var2


def gteq(var1, var2):
    return var1 >= var2


def nteq(var1, var2):
    return var1 != var2


def lst(var1, var2):
    return var1 < var2


def grt(var1, var2):
    return var1 > var2


def eql(var1, var2):
    return var1 == var2


def like(var1, var2):
    if isinstance(var1, int) or isinstance(var2, int) or \
            isinstance(var1, float) or isinstance(var2, float):
        raise TypeError('PARECIO A do not support {0} type'
                        .format(var1.__class__.__name__))
    return var2 in var1


def en(var1, var2):
    return var1 in var2


def betw(var1, rng_start, rng_end):
    return not (var1 <= rng_start or var1 >= rng_end)


def exist(var1, var2):
    return var1 in var2


def y(cond1, cond2):
    return cond1 and cond2


def o(cond1, cond2):
    return cond1 or cond2


OPER = {'<=': lteq, '>=': gteq, '!=': nteq, '<': lst,
        '>': grt, '=': eql, 'PARECIO A': like, 'ENTRE': None,
        'EN': en, 'EXISTE': exist}
CON = {' Y ': y, ' O ': o}\



def count(rows):
    return len(rows)


def average(rows):
    if len(rows) == 0:
        # If there are no values in rows, return 0
        return 0
    else:
        return sum(rows)/len(rows)

FUNC = {'MATS': max, 'MIN': min, 'CONTEA': count, 'PROMEDIO': average}
