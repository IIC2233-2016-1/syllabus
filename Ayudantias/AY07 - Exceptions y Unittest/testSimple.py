import unittest


class ChequearNumeros(unittest.TestCase):
    # este test deberia estar ok
    def test_int_float(self):
        self.assertEquals(1, 1.0)

    # este test debera fallar
    def test_str_float(self):
        self.assertEquals(1, "1")

suite = unittest.TestLoader().loadTestsFromTestCase(ChequearNumeros)
unittest.TextTestRunner().run(suite)
