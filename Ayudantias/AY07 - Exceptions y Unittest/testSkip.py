import unittest
import sys


class IgnorarTests(unittest.TestCase):

    @unittest.expectedFailure
    def test_falla(self):
        self.assertEqual(False, True)

    @unittest.skip("Test inútil")
    def test_ignorar(self):
        self.assertEqual(False, True)
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestCompleto)
unittest.TextTestRunner().run(suite)
