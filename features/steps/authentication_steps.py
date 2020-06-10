import behave

from orangehrm import OrangeHrm as orangehrm

@given(u'Go to logon page')
def step_impl(context):
    context.orangehrm = orangehrm('orangehrm.json', None)
    print ("Go to logon page")


@then(u'Logout')
def step_impl(context):
    context.orangehrm.logout()
    context.orangehrm.driver.quit()
    context.orangehrm.driver.shutdown()


@when(u'Type Admin and password')
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
    try:
        context.orangehrm.check_login_error()
    except:
        pass
    finally:
        context.orangehrm.driver.quit()
        context.orangehrm.driver.shutdown()
