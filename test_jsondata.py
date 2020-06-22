import unittest
from ddt import ddt,file_data

@ddt
class test_loginlogout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('setUpClass')

    @file_data('data/employees.json')
    def test_a_demo(self, lastname, firstname, id, gender, nation, DOB, marital):
        print('demo :', lastname, firstname, id, gender, nation, DOB, marital)

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

if __name__ == '__main__':
    unittest.main()
