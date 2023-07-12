from behave import given, when, then

from simconnect.mock import Mock

@given('The Application is started')
def step_application_started(context):
    context.mock = Mock()
    pass

@given('The Mock is connected')
def step_mock_connected(context):
    context.mock.open()
    assert context.mock._opened is True

@given('A record has started')
def step_record_has_started(context):
    pass

@given('"{time}" has passed')
def step_time_has_passed(context,time):
    pass

@when('The user requests to open the Mock')
def step_request_open_mock(context):
    context.mock.open()

@when('The user requests to close the Mock')
def step_request_close_mock(context):
    context.mock.close()
    pass

@when('The user request to stop the record')
def step_request_stop_record(context):
    pass
		
@then('The Mock is opened')
def step_mock_is_opened(context):
    assert context.mock._opened is True

@then('The Mock is closed')
def step_mock_is_closed(context):
    assert context.mock._opened is False

@then('A correct record is saved')
def step_correct_record_saved(context):
    pass