import unittest
import config

from orangehrm import OrangeHrm as orangehrm
from ddt import ddt, file_data
import random
class test_loginlogout(unittest.TestCase):
    # this method is run before all tests
    @classmethod
    def setUpClass(cls):
        cls.orangehrm = orangehrm()
        cls.orangehrm.home()
        cls.orangehrm.login('admin', cls.orangehrm.application['pwd'])

    # @unittest.skip("debug")#
    def test_a_demo(self):
        self.orangehrm.update_organization_general_information()

    @classmethod
    def tearDownClass(cls):
        cls.orangehrm.logout()
        cls.orangehrm.driver.quit()

if __name__ == '__main__':
    unittest.main()
