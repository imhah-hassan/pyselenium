# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from lib.se_utils import se_utils
import logging
import time
import config

class OrangeHrm (se_utils):
    def __init__(self, driver:None):
        super().__init__()
        self.load_application('orangehrm.json')
        driver = self.get_driver()
        logging.info("Test started")
        logging.info("%s-%s-%s", "Driver loaded", driver.name, driver.session_id)

    def login(self):
        self.driver.get(self.application["url"])
        self.take_screen_shot("home")
        self.type('//input[@id="txtUsername"]', self.application['user'])
        self.type('//input[@id="txtPassword"]', self.application['pwd'])
        self.click('//input[@id="btnLogin"]')
        self.verify_text("//a[@id='welcome']", self.application['messages']["welcomeAdmin"])
        self.take_screen_shot("welcome")

    def logout(self):
        self.click("//a[@id='welcome']")
        self.click("//a[contains(@href, 'auth/logout')]")
        self.driver.quit()

    def change_localization(self):
        self.click("//a[@id='menu_admin_viewAdminModule']")
        self.click("//a[@id='menu_admin_Configuration']")
        self.click("//a[@id='menu_admin_localization']")
        lang = self.get_value("//*[@id='localization_dafault_language']")
        # if localization already in english, do nothing
        # if not set localization to english, otherwise some text verifications will fail
        if (lang == self.application['language']):
            pass
        else:
            self.click ("btnSave")
            self.select("//*[@id='localization_dafault_language']", self.application['language'])
            self.click("btnSave")

    def add_employee(self, lastname, firstname, id, gender, nation, marital, DOB):
        self.click("//a[@id='menu_pim_viewPimModule']")
        time.sleep(0.5)
        self.wait_for_employee_list_load()
        self.click("//a[@id='menu_pim_addEmployee']")
        # En fonction de la vitesse d'exécution.
        # Le 1er click ne permet pas d'afficher la page d'ajouter de l'employee
        if (not self.wait_for_element(By.XPATH, "//input[@id='firstName']")):
            self.click("//a[@id='menu_pim_addEmployee']")
        self.type("//input[@id='firstName']", firstname)
        self.type("//input[@id='lastName']", lastname)
        if (id!=''):
            self.type("//input[@id='employeeId']", id)
        self.click("//*[@id='btnSave']")
        self.take_screen_shot("btnSave")

        # check that Personal Detail page is present
        self.verify_text("//div[@id='pdMainContainer']/div/h1", self.application["messages"]["personalDetails"])
       # check full name in Personal Detail page
        self.verify_text("//div[@id='profile-pic']/h1", firstname + " " + lastname)
        # edit details
        self.click("//input[@id='btnSave']")

        # Le 1er click ne permet pas d'afficher la page de modification du détail de l'employee
        if (not self.wait_for_element(By.XPATH, "//input[@id='personal_optGender_"+str(gender)+"']")):
            self.click("//a[@id='btnSave']")
        self.take_screen_shot("Edit")

        # Gender : male
        self.click("//input[@id='personal_optGender_"+str(gender)+"']")
        # Nation: French
        self.select("//select[@id='personal_cmbNation']", str(nation))
        # Marital status : Single
        self.select("//select[@id='personal_cmbMarital']", marital)
        # Type date of birth
        self.type("//input[@id='personal_DOB']", DOB)
        # Save employee details
        self.click("//input[@id='btnSave']")

    def search_employee(self, id):
        self.click("//a[@id='menu_pim_viewPimModule']")
        self.click("//a[@id='menu_pim_viewEmployeeList']")
        time.sleep(0.3)
        self.wait_for_employee_list_load()
        self.type("//input[@id='empsearch_id']", id)
        self.click("//input[@id='searchBtn']")
        self.wait_for_employee_list_load()
        rowsFound = len(self.driver.find_elements_by_xpath("//table[@id='resultTable']/tbody/tr"))
        logging.warning ("rows : %s" , rowsFound)
        self.verify_numbers(rowsFound, 1)

    def employee_address(self, id):
        self.search_employee(id)
        # details
        self.click("//table[@id='resultTable']/tbody/tr/td[2]/a")
        self.click("//a[contains(@href, 'contactDetails/empNumber')]")
        # Edit
        self.click("//input[@id='btnSave']")
        self.type("//input[@id='contact_street1']", "20 rue de la pomp")
        self.type("//input[@id='contact_city']", "Paris")
        self.type("//input[@id='contact_province']", "Paris")
        self.type("//input[@id='contact_emp_zipcode']", "75001")
        self.select("//select[@id='contact_country']", "FR")
        self.type("//input[@id='contact_emp_hm_telephone']", "0155443322")
        # Save
        self.click("//input[@id='btnSave']")

    def delete_all_employees(self):
        self.click("//a[@id='menu_pim_viewPimModule']")
        time.sleep(0.3)
        self.click("//a[@id='menu_pim_viewEmployeeList']")
        time.sleep(0.3)
        rowsFound = len(self.driver.find_elements_by_xpath("//table[@id='resultTable']/tbody/tr"))
        self.click("//input[@id='ohrmList_chkSelectAll']")
        if (not self.is_selected("//input[@id='ohrmList_chkSelectAll']")):
            time.sleep(0.1)
            self.click("//input[@id='ohrmList_chkSelectAll']")
        self.click("//input[@id='btnDelete']")
        self.click("//input[@id='dialogDeleteBtn']")
        rowsFoundAfterDelete = len(self.driver.find_elements_by_xpath("//table[@id='resultTable']/tbody/tr"))
        if (rowsFoundAfterDelete==rowsFound):
            raise ValueError('Employees not deleted')

    def delete_employee(self, id):
        self.search_employee(id)
        self.click("//table[@id='resultTable']/tbody/tr/td/input")
        self.click("//input[@id='btnDelete']")
        self.click("//input[@id='dialogDeleteBtn']")
        self.assertEqual(self.application["messages"]["NoRecordsFound"], self.get_text("//table[@id='resultTable']/tbody/tr/td"))

    def wait_for_employee_list_load (self):
        count = config.ExplicitWait*10
        element = self.get_element("//input[@id='empsearch_employee_name_empName']")
        cssname = element.get_attribute("class")
        i=1
        while ("ac_loading" in cssname) and (i<count):
            time.sleep(0.1)
            cssname = element.get_attribute("class")
            i=i+1
        if (i<count):
            logging.info("wait_for_employee_list_load : OK", )
            return (True)
        else:
            logging.error("wait_for_employee_list_load : KO")
            return(False)