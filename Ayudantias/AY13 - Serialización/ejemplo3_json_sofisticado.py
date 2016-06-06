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


def object_hook(_dict):
    _dict['dob'] = datetime.fromtimestamp(_dict['dob'])
    return Perro(**_dict)


class Encoder(json.JSONEncoder):
    def default(self, o):
        result = {}
        for k, v in o.__dict__.items():
            if isinstance(v, datetime):
                v = v.timestamp()
            result.update({k: v})
        return result

p = Perro('P-chan', datetime.strptime('01-12-2014', '%d-%m-%Y'), 8.9, 'negro',
          'PUCTerrier', True)
print('Antes de serializar')
print(id(p))
print(p)

print("DUMPS")
p_str = json.dumps(p, cls=Encoder)
print(p_str)

print("LOADS")
p_loads = json.loads(p_str, object_hook=object_hook)
print(id(p_loads))
print(p_loads)

print("DUMP")
with open('p-chan.perrojson', 'w+') as archivo:
    json.dump(p, archivo, cls=Encoder)

print("LOAD")
with open('p-chan.perrojson', 'r+') as archivo:
    p_file = json.load(archivo, object_hook=object_hook)
print(id(p_file))
print(p_file)
