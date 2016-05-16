# Private


class PrivateMeta(type):
    def private_setattr(cls):
        def new_setattr(self, key, value):
            print(cls)
            print(self.__class__.__name__)

            for b in self.__class__.__bases__:
                if b.__name__ != cls:
                    if key in list(b.__dict__.keys()):
                        raise ValueError("No puede cambiar atributos de la clase base")

            self.__dict__[key] = value
        return new_setattr

    def __new__(meta, name, bases, attr):
        print('Creating {0}'.format(name))
        attr['__setattr__'] = meta.private_setattr(name)
        return super().__new__(meta, name, bases, attr)


class A(metaclass=PrivateMeta):
    a = 0
    b = 0

    def __init__(self, a, b):
        print('Clase A')
        print(a)
        print(b)
        A.a = a
        A.b = b


class B(A):
    def __init__(self):
        print('Clase B')
        super().__init__(1, 2)
        self.c = 5
        print('Asignamos c')
        self.a = 4
        self.b = 6


b = B()
a = A(3, 4)
