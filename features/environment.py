import config
from selenium import webdriver
from orangehrm import OrangeHrm as orangehrm

def before_scenario(context, scenario):
    context.orangehrm = orangehrm(config.path+"/orangehrm.json", None)

def after_scenario(context, scenario):
    pass