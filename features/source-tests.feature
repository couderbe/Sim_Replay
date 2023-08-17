Feature: User requests to change the State of the Source

	Scenario: User requests to open the Source - Mock
		Given The Application is started
		When The user requests to open the Mock
		Then The Mock is opened

	Scenario: User requests to close the Source - Mock
		Given The Application is started
		And The Mock is connected
		When The user requests to close the Mock
		Then The Mock is closed