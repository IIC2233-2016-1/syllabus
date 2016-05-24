__author__ = 'cppie_000'

def average(args):
    return sum(args) / len(args)

def setup_module(module):
    module.lista = [1,2,3,4]

def test_average():
    assert average(lista) == 3





