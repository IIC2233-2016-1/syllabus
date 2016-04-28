import unittest


class TestCompleto(unittest.TestCase):

    def setUp(self):
        self.lista = [1, 2, 3, 4]

    def tearDown(self):
        del self.lista

    def test_in_list(self):
        self.assertIn(1, self.lista)

suite = unittest.TestLoader().loadTestsFromTestCase(TestCompleto)
unittest.TextTestRunner().run(suite)
