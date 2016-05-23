from functools import reduce


def constructor(filter_func, lista):

    def decorador(funcion):
        def funcion_nueva(func, iterable):
            new_iterable = list(filter(filter_func, iterable)) + lista
            result = funcion(func, new_iterable)
            return result

        return funcion_nueva

    return decorador


@constructor(lambda x: x % 2 == 0, [6, 7, 8])
def foo(func, iterable):
    return list(map(func, iterable))


@constructor(lambda x: (x+1) % 2 == 1, [9, 8, 10])
def bar(func, iterable):
    return reduce(func, iterable)


if __name__=='__main__':
    print('Ejecutamos el programa')
    print(foo(lambda x: x +1, [1, 2, 3, 5, 8, 13, 21]))
    print(bar(lambda x, y: x - y, [1, 2, 4, 5, 6]))

