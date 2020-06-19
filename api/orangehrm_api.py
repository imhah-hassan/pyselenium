#
# pip install requests Flask
# https://orangehrm.github.io/orangehrm-api-doc/
#
import requests, json
import unittest
import random

class orangehrm_api(unittest.TestCase):
    def __init__(self, url):
        super().__init__()
        self.base_url = url
        # Additional headers.
        headers = {'Content-Type': 'application/json'}
        # data
        payload = {'client_id': 'azertyuiop', 'client_secret': 'azertyuiop', 'grant_type':'client_credentials'}
        resp = requests.post(self.base_url + '/oauth/issueToken', headers=headers, data=json.dumps(payload))
        self.assertEqual(resp.status_code, 200)
        resp = json.loads(resp.content.decode('utf-8'))
        token =  resp['access_token']
        self.access_token = token

    def getEmployee(self, empNumber):
        url = self.base_url + '/api/v1/employee/' + str(empNumber)
        headers = {'Content-Type': 'application/json', 'Authorization':'Bearer ' + self.access_token}
        resp = requests.get(url, headers=headers)
        self.assertEqual(resp.status_code, 200)
        return(json.loads(resp.content.decode('utf-8'))['data'])

    def searchEmployeeByName(self, lastName):
        url = self.base_url + '/api/v1/employee/search'
        headers = {'Content-Type': 'application/json', 'Authorization':'Bearer ' + self.access_token}
        params={'name':lastName}
        resp = requests.get(url, headers=headers, params=params)
        self.assertEqual(resp.status_code, 200)
        return(json.loads(resp.content.decode('utf-8'))['data'])

    def saveEmployee(self, lastName, firstNAme, code):
        url = self.base_url + '/api/v1/employee/0'
        headers = {'Authorization':'Bearer ' + self.access_token}
        payload = {'firstName': firstNAme, 'lastName': lastName, 'code': code}
        resp = requests.post(url, headers=headers, data=payload)
        self.assertEqual(resp.status_code, 200)
        return(resp.status_code)

    def updateEmployeeDetail(self, employeeId):
        url = self.base_url + '/api/v1/employee/' + str(employeeId)
        code = random.randint(1000, 9999)
        headers = {'Authorization':'Bearer ' + self.access_token}
        payload = {'id': employeeId, 'dob': '2000-12-12', 'code':code, 'maritalStatus':'Single', 'gender':'Male', 'nationality':'French'}
        resp = requests.put(url, headers=headers, data=payload)
        self.assertEqual(resp.status_code, 200)
        return(resp.status_code)

    def getEmployeeDetail(self, employeeId):
        url = self.base_url + '/api/v1/employee/' + str(employeeId)
        headers = {'Authorization':'Bearer ' + self.access_token}
        resp = requests.get(url, headers=headers)
        self.assertEqual(resp.status_code, 200)
        return(json.loads(resp.content.decode('utf-8'))['data'])

    def getOrganizationInformation(self):
        url = self.base_url + '/api/v1/organization'
        headers = {'Content-Type': 'application/json', 'Authorization':'Bearer ' + self.access_token}
        resp = requests.get(url, headers=headers)
        self.assertEqual(resp.status_code, 200)
        return(json.loads(resp.content.decode('utf-8'))['data'])

    def terminateEmployment(self, id):
        url = self.base_url + '/api/v1/employee/'+str(id)+'/action/terminate'
        headers = {'Authorization':'Bearer ' + self.access_token}
        payload = {'id': str(id),'date': '2020-07-15', 'reason':'Resigned', 'note':'No comment'}
        resp = requests.post(url, headers=headers, data=payload)
        self.assertEqual(resp.status_code, 200)
        return(resp.content)

    def getEmployeeJobDetail(self, id):
        url = self.base_url + '/api/v1/employee/'+str(id)+'/job-detail'
        headers = {'Authorization':'Bearer ' + self.access_token}
        resp = requests.get(url, headers=headers)
        self.assertEqual(resp.status_code, 200)
        return(json.loads(resp.content.decode('utf-8'))['data'])

    def getCustomers(self):
        url = self.base_url + '/api/v1/customer'
        headers = {'Authorization':'Bearer ' + self.access_token}
        resp = requests.get(url, headers=headers)
        self.assertEqual(resp.status_code, 200)
        return(json.loads(resp.content.decode('utf-8'))['data'])

    def saveCustomer(self, name, description):
        url = self.base_url + '/api/v1/customer'
        headers = {'Authorization':'Bearer ' + self.access_token}
        data = {'name':name, 'description':description}
        resp = requests.post(url, headers=headers, data=data)
        self.assertEqual(resp.status_code, 200)
        return(resp.content)

    def saveProject(self, customerId, name, description):
        url = self.base_url + '/api/v1/project'
        headers = {'Authorization':'Bearer ' + self.access_token}
        data = {'customerId':customerId,'name':name, 'description':description, 'adminIds':1}
        resp = requests.post(url, headers=headers, data=data)
        self.assertEqual(resp.status_code, 200)
        return(resp.content)

    def getProjects(self):
        url = self.base_url + '/api/v1/project'
        headers = {'Authorization':'Bearer ' + self.access_token}
        resp = requests.get(url, headers=headers)
        self.assertEqual(resp.status_code, 200)
        return(json.loads(resp.content.decode('utf-8'))['data'])

    def saveActivity(self, projectId, name):
        url = self.base_url + '/api/v1/activity'
        headers = {'Authorization':'Bearer ' + self.access_token}
        data = {'projectId':projectId,'name':name}
        resp = requests.post(url, headers=headers, data=data)
        self.assertEqual(resp.status_code, 200)
        return(resp.content)

    def deleteActivity(self, projectId, activityId, name):
        url = self.base_url + '/api/v1/activity'
        headers = {'Authorization':'Bearer ' + self.access_token}
        data = {'projectId':projectId,'activityId':activityId, 'name':name}
        resp = requests.delete(url, headers=headers, data=data)
        self.assertEqual(resp.status_code, 202)
        return(resp.content)

    def getActivities(self, projectId):
        url = self.base_url + '/api/v1/activity'
        headers = {'Authorization':'Bearer ' + self.access_token}
        params = {'id':projectId}
        resp = requests.get(url, headers=headers, params=params)
        self.assertEqual(resp.status_code, 200)
        return(json.loads(resp.content.decode('utf-8'))['data'])

    def getTimeSheets(self, employeeId, startDate):
        url = self.base_url + '/api/v1/employee/' + str(employeeId) + '/timesheet'
        headers = {'Authorization':'Bearer ' + self.access_token}
        params = {'startDate':startDate}
        resp = requests.get(url, headers=headers, params=params)
        if (resp.status_code==200):
            return(json.loads(resp.content.decode('utf-8'))['data'])
        else:
            return (resp.reason)

    def saveTimesheet (self, employeeId, startDate):
        url = self.base_url + '/api/v1/employee/' + str(employeeId) + '/timesheet'
        headers = {'Authorization':'Bearer ' + self.access_token}
        params = {'id':employeeId,'startDate':startDate}
        resp = requests.post(url, headers=headers, data=params)
        self.assertEqual(resp.status_code, 200)
        return(resp.content)

    def deleteTimesheetRow (self, projectId, employeeId, activityId, timeSheetId):
        url = self.base_url + '/api/v1/employee/' + str(employeeId) + '/timesheet/row_delete'
        headers = {'Authorization':'Bearer ' + self.access_token}
        data = {'projectId':projectId, 'id':employeeId, 'timesheetId':timeSheetId,'activityId':activityId}
        resp = requests.post(url, headers=headers, data=data)
        self.assertEqual(resp.status_code, 200)
        return(resp.content)

    def updateTimesheet(self, employeeId, startDate):
        url = self.base_url + '/api/v1/employee/' + str(employeeId) + '/timesheet'
        headers = {'Authorization':'Bearer ' + self.access_token}
        data = {
            'employeeId': '1',
            'startDate': startDate,
            'state': 'NOT SUBMITTED',
            'comment': 'No comment',
            'timeSheetItems':
                [
                    {'projectId': '1',
                    'projectActivityId': '1',
                     "0": "17:00", "TimesheetItemId0": "6",
                     "1": "18:00", "TimesheetItemId1": "7",
                     "2": "19:00", "TimesheetItemId2": "8",
                     "3": "21:00", "TimesheetItemId3": "9",
                     "4": "20:00", "TimesheetItemId4": "10",
                     "5": "", "TimesheetItemId5": "",
                     "6": "", "TimesheetItemId6": ""}
                ]
        }
        resp = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(resp.status_code, 200)
        return (resp.content)

    def updateTimesheetStatus(self, employeeId, startDate):
        url = self.base_url + '/api/v1/employee/' + str(employeeId) + '/timesheet'
        headers = {'Authorization':'Bearer ' + self.access_token}
        # possibles state : NOT SUBMITTED, SUBMITTED, APPROVED, REJECTED
        data = {'id':employeeId,
                'startDate':startDate,
                'state':'NOT SUBMITTED',
                'comment':'Update by API'
                }
        resp = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(resp.status_code, 200)
        return (resp.content)
