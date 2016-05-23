def constructor(param1, param2):
    print('Construimos el decorador')

    def decorador(funcion):
        print('Construimos la funcion')

        def funcion_nueva(*args, **kwargs):
            print('Comenzamos')
            print('Usamos los parámetros {0} {1}'.format(param1, param2))
            result = funcion(*args, **kwargs) * 2
            print('Termina ejecución de la función')
            return result

        print('Terminamos de construir la funcion')
        return funcion_nueva

    print('Terminamos de construir el decorador')
    return decorador


@constructor('1', 'y 2')
def foo(a, b):
    return a + b


@constructor('na\' que', 'ver!')
def bar(a, b):
    return a - b


if __name__=='__main__':
    print('Ejecutamos el programa')

    print(foo(2, 3))

    print(bar(2, 6))
