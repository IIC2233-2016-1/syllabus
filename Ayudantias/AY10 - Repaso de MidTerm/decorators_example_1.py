def constructor(param1, param2):
    print('Construimos el decorador')

    def decorador(funcion):
        print('Construimos la funcion')

        def funcion_nueva(*args, **kwargs):
            print('Comenzamos')
            print('Usamos los parámetros\n{0} {1}'.format(param1, param2))
            funcion(*args, **kwargs)
            print('Termina ejecución de la función')

        print('Terminamos de construir la funcion')
        return funcion_nueva

    print('Terminamos de construir el decorador')
    return decorador


@constructor('Esto es ', 'una suma')
def foo(a, b):
    print(a + b)


@constructor('Esto es una resta', '\nNoooo! En serio? ¬¬')
def bar(a, b):
    print(a - b)


if __name__=='__main__':
    print('Ejecutamos el programa')
    foo(2, 3)
    bar(2, 6)
