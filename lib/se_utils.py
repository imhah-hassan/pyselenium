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
            with open(jsonfile, encoding='utf-8') as f:
                self.application = json.load(f)
        except:
            logging.error("file not found %s", jsonfile)

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

    def get_element(self, css):
        time.sleep(config.Latency)
        try:
            self.wait_for_element(By.CSS_SELECTOR, css)
            element = self.driver.find_element_by_css_selector(css)
            return (element)
        except TimeoutException:
            logging.error(self.application['messages']['elementNotFound'], css)

    def get_elements(self, css):
        time.sleep(config.Latency)
        self.wait_for_element(By.css, css)
        elements = self.driver.find_elements_by_css(css)
        return (elements)

    def click(self, css):
        element = self.get_element(css)
        if self.wait_for_element_clickable(By.CSS_SELECTOR, css):
            element.click()
            logging.debug("%s-%s-%s", "Click on", css, self.driver.current_url)

    def type(self, css, value):
        element = self.get_element(css)
        element.click()
        element.clear()
        element.send_keys(value)
        logging.debug("%s-%s-%s", "type", css, value)

    def select(self, css, value):
        element = self.get_element(css)
        Select(element).select_by_value(value)
        logging.debug("%s-%s-%s", "select", css, value)


    def get_text(self, css):
        text = self.get_element(css).text
        logging.debug("%s-%s-%s", "get test", css, text)
        return (text)


    def get_value(self, css):
        value = self.get_element(css).get_attribute("value")
        logging.debug("%s-%s-%s", "get value", css, value)
        return (value)


    def get_count(self, css):
        elements = self.get_elements(css)
        logging.debug("%s-%s-%s", "get count elements", css, len(elements))
        return (len(elements))


    def is_selected(self, css):
        checked = self.driver.find_element_by_css(css).is_selected()
        return checked


    def take_screen_shot(self, name):
        logging.debug("%s-%s-%s", "screen shot", name, 'screenshots\\' + name + '.png')
        self.driver.get_screenshot_as_file('screenshots/' + name + '.png')

    def verify_text(self, css, expected):
        self.assertEqual(expected, self.get_text (css))

    def verify_numbers(self, expected, value):
        self.assertEqual(expected, value)
