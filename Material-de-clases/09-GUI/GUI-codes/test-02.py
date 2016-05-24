__author__ = 'cppie_000'

def average(args):
    return sum(args) / len(args)

def pytest_funcarg__valid_list(request):
    return [1,2,3,4]

def test_average(valid_list):
    assert average(valid_list) == 2.5