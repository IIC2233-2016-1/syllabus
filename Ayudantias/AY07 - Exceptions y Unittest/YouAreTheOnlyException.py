
class Excepcion1(Exception):
    pass

class Excepcion2(Exception):
    def __init__(self, a, b):
        # sobre escribimos el __init__ para cambiar el ingreso de los parmetros
        super().__init__('Alguno de los valores {0} o {1} no son enteros\n'.format(a, b))

class Operaciones:

    def divide(num,den):
        try:
            if not (isinstance(num, int) and isinstance(den, int)):
                raise Excepcion2(num, den)

            if num < 0 or den < 0:
                raise Excepcion1('Los valores son negativos\n')

            return float(num)/float(den)

        except Excepcion1 as err:
            # Este bloque opera para la Excepcion1
            print('Error: {}'.format(err))

        except Excepcion2 as err:
            # Este bloque opera para Excepcion2 cuando los datos no son enteros
            print('Error: {}'.format(err))

        except ZeroDivisionError as err:
            print(type(err))
            print("El denominador es 0")

op1 = Operaciones.divide(4,-3)
op2 = Operaciones.divide(4.4,-3)
op3= Operaciones.divide(1,0)
