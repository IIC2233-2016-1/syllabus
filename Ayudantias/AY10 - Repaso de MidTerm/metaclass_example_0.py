# Metaclases Fácil


class MetaClaseFacil(type):
    def __new__(mcs, name, bases, attr):
        def comer(param):
            def _comer(self):
                self.energia += param
            return _comer

        def new_init(self):
            self.energia = 0

        if Animal in bases:
            if name.startswith('L'):
                attr['comer'] = comer(10)
            elif name.startswith('B'):
                attr['comer'] = comer(20)
            else:
                attr['comer'] = comer(50)
            attr['__init__'] = new_init
            return super().__new__(mcs, name, bases, attr)
        else:
            raise TypeError('No se puede usar esta metaclase para {0}'.format(name))

    def __init__(cls, name, bases, attr):
        print(bases)
        print(attr)
        cls.amigos = bases
        super().__init__(name, bases, attr)

    def __call__(cls, *args, **kwargs):
        print(*args)
        return super().__call__(*args, **kwargs)


class Animal:
    pass


class Burro(Animal, metaclass=MetaClaseFacil):
    pass


class Leon(Animal, metaclass=MetaClaseFacil):
    pass


class Vaca(Animal, metaclass=MetaClaseFacil):
    pass


if __name__ == '__main__':
    b = Burro()
    l = Leon()
    v = Vaca()
    v.comer()
    print(v.energia)
    print(v.amigos)
    print(v.__class__.__dict__)