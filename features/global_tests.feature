Feature: User requests to start the app

	Scenario: User requests to start the app
		Given The Application is fully started
        When The user requests to open the full Mock
        Then The Mock is fully opened
        #And The Application is stopped