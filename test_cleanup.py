import unittest
from orangehrm import OrangeHrm as orangehrm

class test_loginlogout(unittest.TestCase):
    # this method is run before all tests
    @classmethod
    def setUpClass(cls):
        cls.orangehrm = orangehrm()
        cls.orangehrm.home()
        cls.orangehrm.login('admin', cls.orangehrm.application['pwd'])
        cls.employee_id='1360'

    @unittest.skip("debug")
    def test_a_clean_up(self):
        self.orangehrm.clean_up()

    @unittest.skip("debug")
    def test_b_clean_up_company_structure(self):
        self.orangehrm.clean_up_company_structure()
        self.orangehrm.clean_up_company_structure()

    @unittest.skip("debug")
    def test_c_add_location(self):
        self.orangehrm.add_location ('Paris', 'FR', 'Paris', 'Paris', '20 rue des sablons', '01 44 55 44 22')
        self.orangehrm.add_location ('Nantes', 'FR', 'Nantes', 'Nantes', '20 rue des paris', '05 44 55 44 22')

    @unittest.skip("debug")
    def test_d_add_stadd_employment_statusructure(self):
        self.orangehrm.add_structure ('Test.It', 'Test.It', 'Comunauté test')
        self.orangehrm.add_structure ('Strat.Op', 'Strat.Op', 'Comunauté Stratégie')

    @unittest.skip("debug")
    def test_d_add_job_title(self):
        self.orangehrm.add_job_title('Partner', 'Partner', 'Partner')
        self.orangehrm.add_job_title('Leader', 'Leader', 'Leader')
        self.orangehrm.add_job_title('Associate', 'Associate', 'Associate')

    @unittest.skip("debug")
    def test_d_add_employment_status(self):
        self.orangehrm.add_employment_status('CDD')
        self.orangehrm.add_employment_status('CDI')
        self.orangehrm.add_employment_status('Freelance')
        self.orangehrm.add_employment_status('Stagiaire')

    @unittest.skip("debug")
    def test_d_add_job_category(self):
        self.orangehrm.add_job_category('Consultant')
        self.orangehrm.add_job_category('Commercial')
        self.orangehrm.add_job_category('Administratif')
        self.orangehrm.add_job_category('Direction')

    @unittest.skip("debug")
    def test_d_add_customer(self):
        self.orangehrm.add_customer('OrangeHRM', 'OrangeHRM')

    def test_d_add_project(self):
        self.orangehrm.add_project('OrangeHRM', 'Test automation', 'Hassan IMHAH', 'Test AUtomation')

    @unittest.skip("debug")
    def test_e_delete_all_employees(self):
        self.orangehrm.delete_all_employees()

    @unittest.skip("debug")
    def test_i_add_employee(self):
        self.employee_id = self.orangehrm.add_employee('Descartes', 'René', self.employee_id, 1, '64', 'Married', '1596-03-31', 'rdescartes', 'LeDiscoursDeLaMethodes%1632')

    @unittest.skip("debug")
    def test_j_employee_address(self):
        self.orangehrm.employee_address(self.employee_id)

    @unittest.skip("debug")
    def test_j_employee_job(self):
        self.orangehrm.employee_job(self.employee_id)

    @unittest.skip("debug")
    def test_i_login_employee(self):
        self.orangehrm.logout()
        self.orangehrm.login('rdescartes', 'LeDiscoursDeLaMethodes%1632')

    @classmethod
    def tearDownClass(cls):
        cls.orangehrm.logout()
        cls.orangehrm.quit()

if __name__ == '__main__':
    unittest.main()
