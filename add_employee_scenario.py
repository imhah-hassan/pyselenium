import unittest
import xmlrunner

from test_loginlogout import test_loginlogout
# from test_orangehrm import test_orangehrm

# get all tests from SearchText and HomePageTest class
loginlogout = unittest.TestLoader().loadTestsFromTestCase(test_loginlogout)
# add_employee = unittest.TestLoader().loadTestsFromTestCase(test_orangehrm)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([loginlogout])

# run the suite
# unittest.TextTestRunner(verbosity=2).run(test_suite)

# open the report file
# outfile = open("C:\\temp\\SeleniumPythonTestSummary.html", "w")
# configure HTMLTestRunner options
# runner = HTMLTestRunner.HTMLTestRunner(stream=outfile,title='Test Report', description='Acceptance Tests')
# run the suite using HTMLTestRunner
# runner.run(test_suite)

xmlRunner=xmlrunner.XMLTestRunner(output='./xmlreports')
xmlRunner.run(test_suite)