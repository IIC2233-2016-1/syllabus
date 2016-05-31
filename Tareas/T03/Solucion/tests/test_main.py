import unittest
import main
import os


class TestMain(unittest.TestCase):
    def setUp(self):
        self.testConsult = 'test_consult.txt'
        self.testResult = 'test_result.txt'
        self.expectedResult = 'test_expected_results.txt'

    def tearDown(self):
        if os.path.isfile(self.testResult):
            os.remove(self.testResult)

    def test_valid_query(self):
        main.proc_consult_file(self.testConsult, self.testResult)
        # Check result file
        expected_lines = list(open(self.expectedResult, 'r'))
        test_lines = list(open(self.testResult, 'r'))
        self.assertEqual(test_lines, expected_lines)
