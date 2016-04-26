import unittest

class Corrector:

    def __init__(self, nombre):
        self.nombre = nombre

    def chequear_nombre(self):

        return isinstance(self.nombre, str)

class TestCorrector(unittest.TestCase):

    def setUp(self):
        self.archivo = open("archivo.txt", "r")
        self.nombre = "Ariel"
        self.nombre2 = "Daedalus"
        self.instancia = Corrector(self.nombre)
        self.instancia2 = Corrector(self.nombre2)

    def tearDown(self):
        self.archivo.close()

    def test_metodo_chequear_nombre(self):
        self.assertTrue(self.instancia.chequear_nombre())
        self.assertFalse(self.instancia2.chequear_nombre())


suite = unittest.TestLoader().loadTestsFromTestCase(TestCorrector)
unittest.TextTestRunner().run(suite)
