from selenium import webdriver
from orangehrm import OrangeHrm as orangehrm


def before_scenario(context, scenario):
    if 'web' in context.tags:
        context.orangehrm = orangehrm(None)

def after_scenario(context, scenario):
    if 'web' in context.tags:
        context.orangehrm.quit()