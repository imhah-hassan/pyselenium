Feature: OrangeHRM authentication
  As a Administrator, I want to logon to OrangeHRM, and to access to administrator pages.

  Scenario: Conexion to OrangeHRM
    Given Go to logon page
    When Type Admin and password
    Then Check the welcome text and the admin menu