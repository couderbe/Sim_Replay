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

@when('The user requests to close the Mock')
def step_request_close_mock(context):
    context.mock.close()
    pass

@then('The Mock is closed')
def step_mock_is_closed(context):
    assert context.mock._opened is False

