Feature: User requests to record 

	Scenario: User requests to record during 5sec
		Given The Application is started	
		And The Mock is connected
		And A Record has started
		And "2S" has passed
		When The user requests to stop the record
		And The user requests to save the record
		Then "3" correct records are saved
