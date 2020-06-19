Feature: OrangeHRM authentication
  As a Administrator, I want to logon to OrangeHRM, and to access to administrator pages.

  Scenario: Demo feature
    Given Go to logon page
    When Logon as admin
    Then Check the welcome text and the admin menu
    And Logout

