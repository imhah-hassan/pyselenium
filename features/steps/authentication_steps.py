import behave
import config
import features.environment

from orangehrm import OrangeHrm as orangehrm

@when(u'Go to logon page')
@given(u'Go to logon page')
def step_impl(context):
    context.orangehrm.home()

@given(u'Logout')
@then(u'Logout')
def step_impl(context):
    context.orangehrm.logout()
    context.orangehrm.driver.quit()

@given(u'Logon as admin')
@when(u'Logon as admin')
def step_impl(context):
    context.orangehrm.login(context.orangehrm.application['user'], context.orangehrm.application['pwd'])
    context.orangehrm.check_admin_access()

@then(u'Check the welcome text and the admin menu')
def step_impl(context):
    context.orangehrm.check_admin_access()

@when(u'Type Admin and blabla as password')
def step_impl(context):
    context.orangehrm.login(context.orangehrm.application['user'], 'blablabla')

@then(u'Error message displayed')
def step_impl(context):
    context.orangehrm.check_login_error()

@then(u'Close browser')
def step_impl(context):
    context.orangehrm.driver.quit()

@given(u'I create an employee with logn and pwd')
def step_impl(context):
    context.orangehrm.add_employee('LastName', 'FirstName', '', '1', '64', 'Single', '1988-12-14', 'himhah', 'UHYSGpok$23JJ')

@when(u'I logon with employee account')
def step_impl(context):
    context.orangehrm.login('himhah', 'UHYSGpok$23JJ')


@then(u'Check the welcome text and the employee menu')
def step_impl(context):
    context.orangehrm.check_welcome_text('Bienvenue FirstName')
