# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")  # linux only
chrome_options.add_argument("test-type")
driver = driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')

driver.find_element(by=By.NAME, value="username").clear()
driver.find_element(by=By.NAME, value="username").send_keys("Admin")

driver.find_element(by=By.NAME, value="password").clear()
driver.find_element(by=By.NAME, value="password").send_keys("admin123")

driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit']").click()

time.sleep(3)
driver.close()