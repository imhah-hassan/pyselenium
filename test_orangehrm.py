import unittest
from orangehrm import OrangeHrm as orange
from ddt import ddt,file_data

@ddt
class test_orangehrm(unittest.TestCase):
    # this method is run before all tests
    @classmethod
    def setUpClass(cls):
        cls.orangehrm = orange(None)


    def test_a1_login(self):
        self.orangehrm.login()

    @unittest.skip ("deleted")
    def test_a2_delete_allèemployees(self):
        self.orangehrm.delete_all_employees()

    # @unittest.skip("ne changer pas la langue")
    def test_b_change_localization(self):
        self.orangehrm.change_localization()

    def test_c_add_employee(self):
        emp = self.orangehrm.application["employees"][0]
        self.orangehrm.add_employee(emp['lastname'], emp['firstname'], emp['id'], emp['gender'], emp['nation'], emp['marital'], emp['DOB'])


    # @file_data('data\\employees.json')
    # @unittest.skip("debug")
    def test_d_add_employee(self, lastname, firstname, id, gender, nation, marital, DOB):
        self.orangehrm.add_employee(lastname, firstname, id, gender, nation, marital, DOB)


    def test_d_search_employee(self):
        self.orangehrm.search_employee(self.orangehrm.application["employees"][0]["id"])

    def test_z_login(self):
        self.orangehrm.logout()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
