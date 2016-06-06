import json
from datetime import datetime


class Perro:
    def __init__(self, nombre, dob, peso, color, raza, es_hembra):
        self.nombre = nombre
        self.dob = dob
        self.peso = peso
        self.color = color
        self.raza = raza
        self.es_hembra = es_hembra

    def __repr__(self):
        nacida = 'nacida'
        if not self.es_hembra:
            nacida = 'nacido'
        return "{0} - {5} el {4}\nPeso: {1}, Color: {2}, Raza: {3}" \
            .format(self.nombre, self.peso, self.color, self.raza,
                    self.dob.date(),
                    nacida)

    def to_json(self, filename=None):
        _dict = self.__dict__.copy()
        _dict['dob'] = _dict['dob'].timestamp()
        if filename:
            with open(filename + '.perrojson', 'w+') as archivo:
                json.dump(_dict, archivo)
        else:
            return json.dumps(_dict)

    @classmethod
    def from_json(cls, string=None, filename=None):
        if not string and not filename:
            raise ValueError('No se puede cargar un json sin string ni filename')
        if string:
            _dict = json.loads(string)
        else:
            with open(filename, 'r+') as archivo:
                _dict = json.load(archivo)
        _dict['dob'] = datetime.fromtimestamp(_dict['dob'])
        return cls(**_dict)


p = Perro('P-chan', datetime.strptime('01-12-2014', '%d-%m-%Y'), 8.9, 'negro',
          'PUCTerrier', True)
print('Antes de serializar')
print(id(p))
print(p)

print("DUMPS")
p_str = p.to_json()
print(p_str)

print("LOADS")
p_loads = Perro.from_json(string=p_str)
print(id(p_loads))
print(p_loads)

print("DUMP")
p.to_json('p-chan')

print("LOAD")
p_file = Perro.from_json(filename='p-chan.perrojson')
print(id(p_file))
print(p_file)
