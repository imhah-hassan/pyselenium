Feature: OrangeHRM authentication
  As a Administrator, I want to logon to OrangeHRM, and to access to administrator pages.

  Scenario: Logon Error
    Given Go to logon page
    When Type Admin and blabla as password
    Then Error message displayed
    And Close browser

  Scenario: Logon Admin
    Given Go to logon page
    When Logon as admin
    Then Check the welcome text and the admin menu
    And Logout

