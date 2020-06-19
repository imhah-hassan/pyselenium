import unittest
import random
import api.orangehrm_api as api
from orangehrm import OrangeHrm as orangehrm

class test_timesheet_api(unittest.TestCase):
    # this method is run before all tests
    @classmethod
    def setUpClass(cls):
        base_url = 'http://localhost/orangehrm/symfony/web/index.php'
        cls.api = api.orangehrm_api(base_url)
        cls.orangehrm = orangehrm(None)
        cls.code = str(random.randint(1000, 9999))

    @unittest.skip("debug")
    def test_a_saveEmployee(self):
        self.api.saveEmployee('IMHAH' + self.code, 'Hassan', self.code)
        print(self.code)

    @unittest.skip("debug")
    def test_b_set_login(self):
        self.orangehrm.home()
        self.orangehrm.login('admin', self.orangehrm.application['pwd'])
        self.orangehrm.add_employee_login('IMHAH' + self.code)
        self.orangehrm.logout()

    def test_c_login(self):
        self.orangehrm.home()
        self.orangehrm.login(('IMHAH'+self.code).lower(), 'Plqomdk0987$AZE')

    def test_z_logout(self):
        self.orangehrm.logout()
        self.orangehrm.driver.quit()

    @classmethod
    def tearDownClass(cls):
        pass
if __name__ == '__main__':
    unittest.main()
