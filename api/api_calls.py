import api.orangehrm_api as api

api = api.orangehrm_api('http://localhost/orangehrm/symfony/web/index.php')
for customer in api.getCustomers():
    print ("Customer : " + customer['customerId'] + ' - ' + customer['name'] )
for project in api.getProjects():
    print ("Project : " + project['projectId'] + ' - ' + project['projectName'] + ' - ' + project['customerId'] + ' - ' + project['customerName'] )
    for activity in project['activities']:
        print("\t\tactivity : " + activity['id'] + ' - ' + activity['name'])

for employee in api.searchEmployeeByName(''):
    print("employee : " + employee['employeeId'] + ' - ' + employee['code']+ ' - ' + employee['lastName']+ ' - ' + employee['firstName'])
    try:
        for ts in api.getTimeSheets(employee['employeeId'], '2020-05-25'):
            print (api.deleteTimesheetRow(1, 1, 1, ts['timeSheetId']))
            print(ts['timeSheetId'])
    finally:
        pass

# print (api.deleteActivity(1, 1, 'Actvité  1'))
# print (terminateEmployment(1042))
# print (getOrganizationInformation())
# print (searchEmployeeByName('Hassan'))
# print (terminateEmployment(1044))
# print (getEmployeeJobDetail(1044))
# print (getCustomers())
# print(getProjects())
# print(getActivities(1))
# print (saveCustomer('Client 1', 'Clent 1'))
# print (saveProject(1, 'Projet  1', 'Projet 1'))
# print (saveActivity(1, 'Actvité  1'))
# print(saveTimesheet(1, '2020-05-25'))
# print(getTimeSheets(1, '2020-05-25'))
# print(updateTimesheet(1, '2020-05-25'))
# print(updateTimesheetStatus(1, '2020-05-25'))
