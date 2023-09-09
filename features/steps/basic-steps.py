import re
import sys
import time
from behave import given, when, then
from src.main.python.model.model import ModelStatus
from src.main.python.mainQt import MainWindow

class ContextIF:
    """Abstract class representing the context object type
    Used by the IDE
    """
    def __init__(self):
        self.window:MainWindow = None

@given('The Application is started')
def step_application_started(context:ContextIF):
    context.window:MainWindow = MainWindow()
    pass

@given('The Mock is connected')
def step_mock_connected(context:ContextIF):
    context.window.on_connect_mock()
    assert context.window._model.status is ModelStatus.CONNECTED


@given('A record has started')
def step_record_has_started(context:ContextIF):
    context.window._model.start_record([])
    assert context.window._model.status is ModelStatus.RECORDING

@given('"{sec}" has passed')
def step_time_has_passed(context, sec):
    s = int(re.findall(r'-?\d+\.?\d*', sec)[0])
    time.sleep(s)

@given('A file is loaded')
def step_file_is_loaded(context:ContextIF):
    context.window._model.load_file("./features/resources/flight_ex.csv")
    assert context.window._mainTableModel.rowCount() >= 10, "{} is less than {}".format(
        context.window._mainTableModel.rowCount(),10)

@given('the player is started')
def step_player_is_started(context:ContextIF):
    context.window.play_pause()
    assert context.window._model.status is ModelStatus.PLAYING

@when('The user requests to open the Mock')
def step_request_open_full_mock(context:ContextIF):
    context.window.on_connect_mock()


@when('The user requests to close the Mock')
def step_request_close_mock(context:ContextIF):
    context.window.on_connect_mock()


@when('The user requests to stop the record')
def step_request_stop_record(context:ContextIF):
    context.window.record()

@when('The user requests to stop the player')
def step_request_stop_player(context:ContextIF):
    context.window.play_pause()

@when('The user requests to save the record')
def step_request_save_record(context:ContextIF):
    context.window._model.save_file("./build/Test.csv")


@then('The Mock is opened')
def step_mock_is_opened(context:ContextIF):
    assert context.window._model.status is ModelStatus.CONNECTED


@then('The Mock is closed')
def step_mock_is_closed(context:ContextIF):
    assert context.window._model.status is ModelStatus.OFFLINE

@then('The player is stopped')
def step_player_is_stopped(context:ContextIF):
    assert context.window._model.status is ModelStatus.CONNECTED
    assert context.window._model._player.current_record > 0

@then('"{nbr}" correct records are saved')
def step_correct_record_saved(context:ContextIF,nbr:str):
    assert context.window._mainTableModel.rowCount() >= int(nbr), "{} is less than {}".format(
        context.window._mainTableModel.rowCount(),nbr)
    with open('./build/Test.csv', 'r') as csvfile:
        for line in csvfile.readlines()[1:]:
            splitted = line.split(';')
            for d in splitted:
                assert isfloat(d)


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
