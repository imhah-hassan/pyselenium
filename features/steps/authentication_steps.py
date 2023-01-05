from behave import *
@when(u'Go to logon page')
@given(u'Go to logon page')
def step_impl(context):
    ctx = context.orangehrm
    ctx.home()

@given(u'Logout')
@then(u'Logout')
def step_impl(context):
    ctx = context.orangehrm
    ctx.logout()
    ctx.driver.quit()

@given(u'Logon as admin')
@when(u'Logon as admin')
def step_impl(context):
    ctx = context.orangehrm
    ctx.login(ctx.application['user'], ctx.application['pwd'])
    ctx.check_admin_access()

@then(u'Check the welcome text and the admin menu')
def step_impl(context):
    ctx = context.orangehrm
    ctx.check_admin_access()

@when(u'Type Admin and blabla as password')
def step_impl(context):
    ctx = context.orangehrm
    ctx.login(ctx.application['user'], 'blablabla')

@then(u'Error message displayed')
def step_impl(context):
    ctx = context.orangehrm
    ctx.check_login_error()

@then(u'Close browser')
def step_impl(context):
    ctx = context.orangehrm
    ctx.driver.quit()

@given(u'I create an employee with logn and pwd')
def step_impl(context):
    ctx = context.orangehrm
    ctx.add_employee('LastName', 'FirstName', '', '1', '64', 'Single', '1988-12-14', 'himhah', 'UHYSGpok$23JJ')

@when(u'I logon with employee account')
def step_impl(context):
    ctx = context.orangehrm
    ctx.login('himhah', 'UHYSGpok$23JJ')


@then(u'Check the welcome text and the employee menu')
def step_impl(context):
    ctx = context.orangehrm
    ctx.check_welcome_text('Bienvenue FirstName')
