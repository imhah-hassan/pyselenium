import behave

from orangehrm import OrangeHrm as orangehrm

@given(u'Go to logon page')
def step_impl(context):
    # context.orangehrm = orangehrm('../orangehrm.json', None)
    print ("Go to logon page")


@when(u'Type Admin and password')
def step_impl(context):
    # context.orangehrm.login()
    print ("Type Admin and password")


@then(u'Check the welcome text and the admin menu')
def step_impl(context):
    # context.orangehrm.check_admin_access()
    print ("Check the welcome text and the admin menu")
