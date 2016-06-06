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