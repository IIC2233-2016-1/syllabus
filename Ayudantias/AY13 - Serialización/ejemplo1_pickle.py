import pickle
from datetime import datetime


class Perro:
    def __init__(self, nombre, dob, peso, color, raza, es_hembra):
        self.nombre = nombre
        self.dob = dob
        self.peso = peso
        self.color = color
        self.raza = raza
        self.es_hembra = es_hembra

    def __getstate__(self):
        a_guardar = self.__dict__.copy()
        hoy = datetime.now()
        a_guardar.update(
            {'fechaAlmacenamiento': (hoy.day, hoy.month, hoy.year)})
        return a_guardar

    def __setstate__(self, nuevo):
        hoy = datetime.now()
        print('Hora de Deserialización:', str(hoy.hour) + ':' + str(hoy.minute),
              "{0}-{1}-{2}".format(hoy.day, hoy.month, hoy.year))
        self.__dict__ = nuevo

    def __repr__(self):
        nacida = 'nacida'
        if not self.es_hembra:
            nacida = 'nacido'
        return "{0} - {5} el {4}\nPeso: {1}, Color: {2}, Raza: {3}" \
            .format(self.nombre, self.peso, self.color, self.raza,
                    self.dob.date(),
                    nacida)


p = Perro('P-chan', datetime.strptime('01-12-2014', '%d-%m-%Y'), 8.9, 'negro',
          'PUCTerrier', True)
print(id(p))
print(p)

p_str = pickle.dumps(p)
print(p_str)
print(id(pickle.loads(p_str)))
print(pickle.loads(p_str))

with open('p-chan.perro', 'wb') as archivo:
    pickle.dump(p, archivo)

with open('p-chan.perro', 'rb') as archivo:
    p_file = pickle.load(archivo)
print(id(p_file))
print(p_file)
