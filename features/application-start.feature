Feature: The Application is started - mock opening
  
	Scenario: User request to close the Mock
		Given The Application is started
		And The Mock is connected
		When The user requests to close the Mock
		Then The Mock is closed