import json

class Perro:
    def __init__(self, nombre, dob, peso, color, raza, es_hembra):
        self.nombre = nombre
        self.dob = dob
        self.peso = peso
        self.color = color
        self.raza = raza
        self.es_hembra = es_hembra

    @classmethod
    def load_from_json(cls, dict):
        cls(**dict)

    def __repr__(self):
        nacida = 'nacida'
        if not self.es_hembra:
            nacida = 'nacido'
        return "{0} - {5} el {4}\nPeso: {1}, Color: {2}, Raza: {3}" \
            .format(self.nombre, self.peso, self.color, self.raza,
                    self.dob,
                    nacida)

p = Perro('P-chan', '01-12-2014', 8.9, 'negro', 'PUCTerrier', True)
print(id(p))
print(p)

p_str = json.dumps(p.__dict__)
print(p_str)
print(id(json.loads(p_str)))
print(json.loads(p_str))

with open('p-chan.perrojson', 'w+') as archivo:
    json.dump(p.__dict__, archivo)

with open('p-chan.perrojson', 'r') as archivo:
    p_file = json.load(archivo)
print(id(p_file))
print(p_file)

