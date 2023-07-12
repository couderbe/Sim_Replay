Feature: User requests to record 

	Scenario: User requests to record during 5sec
		Given The Application is started	
		And The Mock is connected
		And A Record has started
		And "5S" has passed
		When The user request to stop the record
		Then A correct record is saved
