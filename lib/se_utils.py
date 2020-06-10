# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from logging.handlers import RotatingFileHandler
import unittest
import logging
import time
import json
import config
import warnings
from pathlib import Path
import os

class se_utils (unittest.TestCase):

    def __init__(self):
        super().__init__()
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        self.driver = None
        self.application = None
        Path("./logs").mkdir(parents=True, exist_ok=True)
        logfile = "logs/orangehrm.log"
        logger = logging.getLogger(logfile)
        handler = RotatingFileHandler(logfile, maxBytes=2000000, backupCount=10)
        logger.addHandler(handler)
        fmt = '%(asctime)s.%(msecs)03d;%(levelname)s;%(module)s;%(message)s'
        logging.basicConfig(format=fmt, datefmt='%Y.%m.%d %H.%M.%S', filename=logfile, level=config.LogLevel)

    def quit(self):
        self.driver.quit()

    def load_application (self, jsonfile):
        print ("Current dir : " + os.getcwd())
        with open(jsonfile, encoding='utf-8') as f:
            self.application = json.load(f)

    def get_driver (self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("test-type")
        if (config.Headless):
            chrome_options.add_argument("--headless")
        if (config.Remote==''):
            driver = webdriver.Chrome("../drivers/chromedriver.exe", chrome_options=chrome_options)
        else:
            driver = webdriver.Remote(
                command_executor=config.Remote,
                desired_capabilities=chrome_options.to_capabilities())
        driver.implicitly_wait(config.ImplicitWait)
        self.driver = driver
        return (driver)

    def wait_for_element(self, by, locator):
        try:
            WebDriverWait(self.driver, config.ExplicitWait).until(EC.presence_of_element_located((by, locator)))
            logging.debug("%s-%s-%s", self.application['messages']['elementFound'], by, locator)
        except TimeoutException:
            logging.error("%s-%s-%s", self.application['messages']['elementNotFound'], by, locator)
            return (False)

        try:
            WebDriverWait(self.driver, config.ExplicitWait).until(EC.visibility_of_element_located((by, locator)))
            logging.debug("%s-%s-%s", self.application['messages']['elementVisible'], by, locator)
            return (True)
        except TimeoutException:
            logging.error("%s-%s-%s", self.application['messages']['elementNotVisible'], by, locator)
            return (False)

    def wait_for_element_clickable(self, by, locator):
        try:
            WebDriverWait(self.driver, config.ExplicitWait).until(EC.element_to_be_clickable((by, locator)))
            logging.debug("%s-%s-%s", self.application['messages']['elementClickable'], by, locator)
            return (True)
        except TimeoutException:
            logging.error("%s-%s-%s", self.application['messages']['elementNotClickable'], by, locator)

    def get_element(self, xpath):
        time.sleep(config.Latency)
        try:
            self.wait_for_element(By.XPATH, xpath)
            element = self.driver.find_element_by_xpath(xpath)
            return (element)
        except TimeoutException:
            logging.error(self.application['messages']['elementNotFound'], xpath)

    def get_elements(self, xpath):
        time.sleep(config.Latency)
        self.wait_for_element(By.XPATH, xpath)
        elements = self.driver.find_elements_by_xpath(xpath)
        return (elements)

    def click(self, xpath):
        element = self.get_element(xpath)
        if self.wait_for_element_clickable(By.XPATH, xpath):
            element.click()
            logging.debug("%s-%s-%s", "Click on", xpath, self.driver.current_url)

    def type(self, xpath, value):
        element = self.get_element(xpath)
        element.click()
        element.clear()
        element.send_keys(value)
        logging.debug("%s-%s-%s", "type", xpath, value)

    def select(self, xpath, value):
        element = self.get_element(xpath)
        Select(element).select_by_value(value)
        logging.debug("%s-%s-%s", "select", xpath, value)


    def get_text(self, xpath):
        text = self.get_element(xpath).text
        logging.debug("%s-%s-%s", "get test", xpath, text)
        return (text)


    def get_value(self, xpath):
        value = self.get_element(xpath).get_attribute("value")
        logging.debug("%s-%s-%s", "get value", xpath, value)
        return (value)


    def get_count(self, xpath):
        elements = self.get_elements(xpath)
        logging.debug("%s-%s-%s", "get count elements", xpath, len(elements))
        return (len(elements))


    def is_selected(self, xpath):
        checked = self.driver.find_element_by_xpath(xpath).is_selected()
        return checked


    def take_screen_shot(self, name):
        logging.debug("%s-%s-%s", "screen shot", name, 'screenshots\\' + name + '.png')
        self.driver.get_screenshot_as_file('screenshots/' + name + '.png')

    def verify_text(self, xpath, expected):
        self.assertEqual(expected, self.get_text (xpath))

    def verify_numbers(self, expected, value):
        self.assertEqual(expected, value)
