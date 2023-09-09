Feature: User requests to play 

	Scenario: User requests to play during 5sec
		Given The Application is started	
		And A file is loaded
		And The Mock is connected
		And the player is started
		And "2S" has passed
		When The user requests to stop the player
		Then the player is stopped
