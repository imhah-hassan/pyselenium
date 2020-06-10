import unittest

from orangehrm import OrangeHrm as orangehrm
from ddt import ddt, file_data
import random
class test_loginlogout(unittest.TestCase):
    # this method is run before all tests
    @classmethod
    def setUpClass(cls):
        cls.idEmployee=random.randint(1000, 9999)
        cls.orangehrm = orangehrm(None)

    def test_a_login(self):
        self.orangehrm.login()

    def test_b_add_employee(self):
        self.orangehrm.add_employee('essai', 'premier', str(self.idEmployee), 1, 64, 'Single', '1976-04-27')

    # @unittest.skip("debug")
    def test_c_search_employee(self):
        self.orangehrm.search_employee(self.idEmployee)

    def test_d_employee_address(self):
        self.orangehrm.employee_address(self.idEmployee)

    def test_e_delete_employee(self):
        self.orangehrm.delete_employee(str(self.idEmployee))

    def test_z_logout(self):
        self.orangehrm.logout()

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
