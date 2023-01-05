# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from lib.se_utils import se_utils
import logging
import time
import config
import os

class OrangeHrm (se_utils):
    def __init__(self):
        super().__init__()
        self.load_application('orangehrm.json')
        self.driver = self.get_driver()
        logging.info("Test started")
        logging.debug("%s-%s-%s", "Driver loaded", self.driver.name, self.driver.session_id)

    # common actions
    def home(self):
        self.driver.get(self.application["url"])

    def navigate(self, relative_path):
        self.driver.get(self.application["url"]+relative_path)

    def login(self, username, password):
        logging.info("login to : %s with use %s ",  self.application["url"], self.application["user"])
        self.take_screen_shot("home")
        self.type("#txtUsername", username)
        self.type("#txtPassword", password)
        self.click("#btnLogin")
        time.sleep(2)

    def check_admin_access (self):
        self.verify_text("#welcome", self.application['messages']["welcomeAdmin"])
        self.take_screen_shot("welcome")

    def check_login_error (self):
        self.verify_text("#spanMessage", self.application['messages']["logonError"])
        self.take_screen_shot("LogonError")

    def quit(self):
        self.driver.quit()

    def logout(self):
        logging.info("logout and quit")
        self.click("#welcome")
        self.click("//a[contains(@href, 'auth/logout')]")

    def change_localization(self):
        logging.info("change_localization to : %s", self.application['language'])
        self.click("#menu_admin_viewAdminModule")
        self.click("#menu_admin_Configuration")
        self.click("#menu_admin_localization")
        lang = self.get_value("//*[@id='localization_dafault_language")
        # if localization already in english, do nothing
        # if not set localization to english, otherwise some text verifications will fail
        if (lang == self.application['language']):
            pass
        else:
            self.click ("btnSave")
            self.select("//*[@id='localization_dafault_language']", self.application['language'])
            self.click("btnSave")

    def delete_all_items (self):
        msg = self.get_text('td').lower()
        if (msg != u"aucun résultat"):
            self.click('#ohrmList_chkSelectAll')
            self.click('#btnDelete')
            self.click('#dialogDeleteBtn')
            self.verify_text('td', u"Aucun résultat")

    # Clean up
    def clean_up (self):
        self.navigate('/admin/viewJobTitleList')
        self.delete_all_items()
        self.navigate('/admin/viewPayGrades')
        self.delete_all_items()
        self.navigate('/admin/employmentStatus')
        self.delete_all_items()
        self.navigate('/admin/jobCategory')
        self.delete_all_items()
        self.navigate('/admin/viewLocations')
        self.delete_all_items()
        self.navigate('/admin/viewCustomers')
        self.delete_all_items()

    def clean_up_company_structure (self):
        self.navigate('/admin/viewCompanyStructure')
        self.click ('#btnEdit')
        try:
            element = self.get_element('.deleteButton')
            while (element):
                self.click('.deleteButton')
        except :
            pass

    # Configure
    def add_location (self, name, country, province, city, address, phone):
        self.navigate('/admin/viewLocations')
        self.click('#btnAdd')
        self.type('#location_name', name)
        self.select('#location_country',country)
        self.type('#location_province',province)
        self.type('#location_city',city)
        self.type('#location_address',address)
        self.type('#location_phone',phone)
        self.click('#btnSave')

    def add_structure (self, unit_id, unit_name, unit_description):
        self.navigate('/admin/viewCompanyStructure')
        self.click('#btnEdit')
        self.click('.addButton')
        self.type('#txtUnit_Id',unit_id)
        self.type('#txtName',unit_name)
        self.type('#txtDescription',unit_description)
        self.click('#btnSave')

    def add_job_title(self, title, description, note):
        self.navigate("/admin/viewJobTitleList")
        self.click("#menu_admin_viewAdminModule")
        self.click("#menu_admin_Job")
        self.click("#menu_admin_viewJobTitleList")
        self.click("#btnAdd")
        self.type("#jobTitle_jobTitle", title)
        self.type("#jobTitle_jobDescription", description)
        self.type("#jobTitle_note", note)
        self.click("#btnSave")

    def add_employment_status(self, title):
        self.navigate("/admin/employmentStatus")
        self.click("#menu_admin_viewAdminModule")
        self.click("#menu_admin_Job")
        self.click("#menu_admin_employmentStatus")
        self.click("#btnAdd")
        self.type("#empStatus_name", title)
        self.click("#btnSave")

    def add_job_category(self, category):
        self.navigate("/admin/jobCategory")
        self.click("#menu_admin_viewAdminModule")
        self.click("#menu_admin_Job")
        self.click("#menu_admin_jobCategory")
        self.click("#btnAdd")
        self.type("#jobCategory_name", category)
        self.click("#btnSave")

    def add_customer(self, name, description):
        self.navigate("/admin/viewCustomers")
        self.click("#menu_time_viewTimeModule")
        self.click("#menu_admin_ProjectInfo")
        self.click("#menu_admin_viewCustomers")
        self.click("#btnAdd")
        self.type("#addCustomer_customerName", name)
        self.type("#addCustomer_description", description)
        self.click("#btnSave")

    def add_project(self, customer_name, project_name, administrator, description):
        self.navigate("/admin/viewProjects")
        self.click("#menu_time_viewTimeModule")
        self.click("#menu_admin_ProjectInfo")
        self.click("#menu_admin_viewProjects")
        self.click("#btnAdd")
        self.type("#addProject_customerName", customer_name)
        self.type("#addProject_projectName", project_name)
        self.type("#addProject_projectAdmin_1", administrator)
        self.type("#addProject_description", description)
        self.click("#btnSave")

    def add_employee(self, lastname, firstname, id, gender, nation, marital, DOB, username, password):
        logging.info("add employee  : %s %s", lastname, firstname)
        self.wait_for_employee_list_load()
        self.click("#menu_pim_addEmployee")
        self.type("#firstName", firstname)
        self.type("#lastName", lastname)
        if (id!=''):
            self.type("#employeeId", id)
        else:
            id=self.get_value('#employeeId')

        explicitWait = config.ExplicitWait
        if (username!=''):
            self.click('#chkLogin')
            self.type("#user_name", username)
            self.type("#user_password", password)
            self.type("#re_password", password)
            self.click("#btnSave")
            config.ExplicitWait = 30
            self.wait_for_element(By.XPATH, '//div[@id="pdMainContainer"]/div/h1')
        else:
            self.click("#btnSave")

        config.ExplicitWait = explicitWait
        self.take_screen_shot("btnSave")

        # check that Personal Detail page is present
        self.verify_text("//div[@id='pdMainContainer']/div/h1", self.application["messages"]["personalDetails"])
       # check full name in Personal Detail page
        self.verify_text("//div[@id='profile-pic']/h1", firstname + " " + lastname)
        # edit details
        self.click("#btnSave")

        # Le 1er click ne permet pas d'afficher la page de modification du d�tail de l'employee
        if (not self.wait_for_element(By.CSS_SELECTOR, "#personal_optGender_"+str(gender)+"")):
            self.click("#btnSave")
        self.take_screen_shot("Edit")

        # Gender : male
        self.click("#personal_optGender_"+str(gender)+"")
        # Nation: French
        self.select("//select[@id='personal_cmbNation']", str(nation))
        # Marital status : Single
        self.select("//select[@id='personal_cmbMarital']", marital)
        # Type date of birth
        self.type("#personal_DOB", DOB)
        # Save employee details
        self.click("#btnSave")
        return (id)

    def search_employee(self, id):
        logging.info("search employee by id : %s", id)
        self.click("#menu_pim_viewPimModule")
        self.click("#menu_pim_viewEmployeeList")
        self.wait_for_employee_list_load()
        self.type("#empsearch_id", id)
        self.click("#searchBtn")
        self.wait_for_employee_list_load()
        rowsFound = len(self.driver.find_elements(By.XPATH, "//table[@id='resultTable']/tbody/tr"))
        logging.info("rows found : %s", rowsFound)
        self.verify_numbers(rowsFound, 1)

    def employee_address(self, id):
        logging.info("update employee address : %s", id)
        self.search_employee(id)
        # details
        self.click("//table[@id='resultTable']/tbody/tr/td[2]/a")
        self.click("//a[contains(@href, 'contactDetails/empNumber')]")
        # Edit
        self.click("#btnSave")
        self.type("#contact_street1", "20 rue de la pomp")
        self.type("#contact_city", "Paris")
        self.type("#contact_province", "Paris")
        self.type("#contact_emp_zipcode", "75001")
        self.select("#contact_country", "FR")
        self.type("#contact_emp_hm_telephone", "0155443322")
        # Save
        self.click("#btnSave")

    def employee_job(self, employee_id):
        logging.info("add job : %s", employee_id)
        self.search_employee(employee_id)
        # details
        self.click("//table[@id='resultTable']/tbody/tr/td[2]/a")
        self.click("//a[contains(@href, 'pim/viewJobDetails/empNumber')]")
        self.click("#btnSave")
        self.select_text("#job_job_title", "Associate")
        self.select_text("#job_emp_status", "CDI")
        self.select_text("#job_eeo_category", "Consultant")
        self.select_text("#job_sub_unit", "Test.It")
        self.select_text("#job_location", "Paris")
        self.type("#job_contract_start_date", "2020-07-01")
        self.click("#btnSave")

    def delete_all_employees(self):
        logging.info("delete all employees")
        self.click("#menu_pim_viewPimModule")
        time.sleep(0.3)
        self.click("#menu_pim_viewEmployeeList")
        time.sleep(0.3)
        rowsFound = len(self.driver.find_elements_by_xpath("//table[@id='resultTable']/tbody/tr"))
        self.click("#ohrmList_chkSelectAll")
        if (not self.is_selected("#ohrmList_chkSelectAll")):
            time.sleep(0.1)
            self.click("#ohrmList_chkSelectAll")
        self.click("#btnDelete")
        self.click("#dialogDeleteBtn")
        rowsFoundAfterDelete = len(self.driver.find_elements_by_xpath("//table[@id='resultTable']/tbody/tr"))
        if (rowsFoundAfterDelete==rowsFound):
            raise ValueError('Employees not deleted')

    def delete_employee(self, id):
        logging.info("delete employee by id : %s", id)
        self.search_employee(id)
        self.click("//table[@id='resultTable']/tbody/tr/td/input")
        self.click("#btnDelete")
        self.click("#dialogDeleteBtn")
        self.assertEqual(self.application["messages"]["NoRecordsFound"], self.get_text("//table[@id='resultTable']/tbody/tr/td"))

    def wait_for_employee_list_load (self):
        logging.info("wait for employee list load")
        self.navigate('/pim/viewEmployeeList')
        count = config.ExplicitWait*10
        try:
            element = self.get_element("button[type='button'] i.bi-plus")
            return (True)
        except:
            logging.error("wait_for_employee_list_load : KO")
            return(False)

    # TODO : add code
    def update_organization_general_information(self):
        pass