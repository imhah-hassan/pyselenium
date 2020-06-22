# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
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

        Path(config.path +  "/logs").mkdir(parents=True, exist_ok=True)
        logfile = config.path + "/logs/orangehrm.log"
        handler = logging.handlers.WatchedFileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d;%(levelname)s;%(module)s;%(funcName)s;%(lineno)d;%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        root = logging.getLogger()
        root.setLevel(config.LogLevel)
        root.addHandler(handler)

        logging.info("Test started")
        logging.info("Current path : %s", os.getcwd())

    def load_application (self, jsonfile):
        try:
            with open(config.path + '\\' + jsonfile, encoding='utf-8') as f:
                self.application = json.load(f)
        except:
            logging.error("file not found %s", jsonfile)

    def navigate (self, relative_url):
        self.driver.get (self.application['url'] + relative_url)

    def get_driver (self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("test-type")
        if (config.Headless):
            chrome_options.add_argument("--headless")
        logging.info("Driver path : %s/drivers/chromedriver.exe", config.path)
        try:
            if (config.Remote==''):
                driver = webdriver.Chrome(config.path + "/drivers/chromedriver.exe", options=chrome_options)
            else:
                driver = webdriver.Remote(
                    command_executor=config.Remote,
                    desired_capabilities=chrome_options.to_capabilities())
        except WebDriverException as e:
            logging.error(e.msg)
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

    def get_element(self, locator):
        time.sleep(config.Latency)
        try:
            if (locator.startswith('id=')):
                locator = locator.replace('id=', '')
                self.wait_for_element(By.ID, locator)
                element = self.driver.find_element_by_id(locator)
            else:
                if (locator.startswith('//')):
                    self.wait_for_element(By.XPATH, locator)
                    element = self.driver.find_element_by_xpath(locator)
                else:
                    self.wait_for_element(By.CSS_SELECTOR, locator)
                    element = self.driver.find_element_by_css_selector(locator)
            return (element)
        except TimeoutException:
            logging.error(self.application['messages']['elementNotFound'], locator)

    def get_elements(self, locator):
        time.sleep(config.Latency)
        self.wait_for_element(By.XPATH, locator)
        elements = self.driver.find_elements_by_xpath(locator)
        return (elements)

    def click(self, locator):
        element = self.get_element(locator)
        isClickable=False
        if (locator.startswith('id=')):
            locator = locator.replace('id=', '')
            isClickable = self.wait_for_element_clickable(By.ID, locator)
        else:
            if(locator.startswith('//')):
                isClickable = self.wait_for_element_clickable(By.XPATH, locator)
            else:
                isClickable = self.wait_for_element_clickable(By.CSS_SELECTOR, locator)
        # is clickable
        if isClickable:
            element.click()
            logging.debug("%s-%s-%s", "Click on", locator, self.driver.current_url)

    def type(self, locator, value):
        element = self.get_element(locator)
        element.click()
        element.clear()
        element.send_keys(value)
        logging.debug("%s-%s-%s", "type", locator, value)

    def select(self, locator, value):
        element = self.get_element(locator)
        Select(element).select_by_value(value)
        logging.debug("%s-%s-%s", "select", locator, value)

    def get_text(self, locator):
        text = self.get_element(locator).text
        logging.debug("%s-%s-%s", "get test", locator, text)
        return (text)

    def get_value(self, locator):
        value = self.get_element(locator).get_attribute("value")
        logging.debug("%s-%s-%s", "get value", locator, value)
        return (value)

    def get_count(self, locator):
        elements = self.get_elements(locator)
        logging.debug("%s-%s-%s", "get count elements", locator, len(elements))
        return (len(elements))

    def is_selected(self, locator):
        checked = self.driver.find_element_by_xpath(locator).is_selected()
        return checked

    def take_screen_shot(self, name):
        logging.debug("%s-%s-%s", "screen shot", name, 'screenshots\\' + name + '.png')
        self.driver.get_screenshot_as_file('screenshots/' + name + '.png')

    def verify_text(self, locator, expected):
        self.assertEqual(expected, self.get_text (locator))

    def verify_numbers(self, expected, value):
        self.assertEqual(expected, value)
