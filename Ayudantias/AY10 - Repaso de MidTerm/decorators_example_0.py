
def decorador(funcion):
    print('Construimos la funcion')

    def funcion_nueva(*args, **kwargs):
        print('Comenzamos con la ejecución de la función')
        funcion(*args, **kwargs)
        print('Termina ejecución de la función')

    print('Terminamos de construir la funcion')
    return funcion_nueva

@decorador
def foo(a, b):
    print(a + b)


@decorador
def bar(a, b):
    print(a - b)

if __name__=='__main__':
    print('Ejecutamos el programa')
    foo(2, 3)
    bar(2, 6)