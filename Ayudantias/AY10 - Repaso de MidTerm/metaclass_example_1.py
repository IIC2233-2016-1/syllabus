# Final class


class FinalObjectMeta(type):

    def __new__(meta, name, bases, attr):
        def new_setattr(self, key, value):
            raise ValueError("Cannot change attributes")
        attr['__setattr__'] = new_setattr
        # Esto no logra el comportamiento que queremos.
        return super().__new__(meta, name, bases, attr)

    def __call__(self, *args, **kwargs):
        def traditional_setattr(self, key, value):
            self.__dict__[key] = value

        def new_setattr(self, key, value):
            raise ValueError("Cannot change attributes")

        # setattr(self, '__setattr__', traditional_setattr)
        new_instance = super().__call__(*args, **kwargs)
        # setattr(self, '__setattr__', new_setattr)
        return new_instance


class A(metaclass=FinalObjectMeta):
    def __init__(self, a, b):
        self.a = a
        self.b = b


if __name__ == '__main__':
    a = A(1, 2)
    a.a = 2
