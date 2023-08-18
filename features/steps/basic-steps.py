import re
import time
from behave import given, when, then
from src.main.python.outputs import save_datas
from src.main.python.recorder import Recorder
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from src.main.python.simconnect.mock import Mock, Mock_Value


@given('The Application is started')
def step_application_started(context):
    context.mock = Mock()
    pass


@given('The Mock is connected')
def step_mock_connected(context):
    context.mock.open()
    context.mock.add_listened_parameter("ZULU TIME","s",None,None,1,1,1000000,False)
    context.mock.add_listened_parameter("Plane Latitude","°",None,None,40,40,60)
    context.mock.add_listened_parameter("Plane Longitude","°",None,None,0,0,10)
    context.mock.add_listened_parameter("Plane Altitude","ft",None,None,1000,1000,2000)
    context.mock.add_listened_parameter("Plane Bank Degrees","°",None,None,-60,-60,60)
    context.mock.add_listened_parameter("Plane Pitch Degrees","°",None,None,-20,-20,20)
    context.mock.add_listened_parameter("Plane Heading Degrees True","°",None,None,10,10,355)        
    context.mock.start()
    assert context.mock._opened is True


@given('A record has started')
def step_record_has_started(context):
    context._mainTableModel = QStandardItemModel()
    parameters_to_record = [
        "ZULU TIME",
        "Plane Longitude",
        "Plane Latitude",
        "Plane Altitude",
        "Plane Bank Degrees",
        "Plane Pitch Degrees",
        "Plane Heading Degrees True"]
    
    context._mainTableModel.appendRow(
                    [QStandardItem("a") for _ in range(len(parameters_to_record))])

    for i, header in enumerate(parameters_to_record):
        context._mainTableModel.setHeaderData(
            i, Qt.Orientation.Horizontal, header)
        
    context._mainTableModel.removeRow(0)
    
    context.recorder = Recorder(
        context.mock, context._mainTableModel, parameters_to_record)

    context.recorder.start()
    assert context.recorder._stop_flag is False


@given('"{sec}" has passed')
def step_time_has_passed(context, sec):
    s = int(re.findall(r'-?\d+\.?\d*', sec)[0])
    time.sleep(s)


@when('The user requests to open the Mock')
def step_request_open_mock(context):
    context.mock.open()


@when('The user requests to close the Mock')
def step_request_close_mock(context):
    context.mock.close()


@when('The user requests to stop the record')
def step_request_stop_record(context):
    context.recorder.stop()


@when('The user requests to save the record')
def step_request_save_record(context):
    save_datas("./build/Test.csv", context._mainTableModel)


@then('The Mock is opened')
def step_mock_is_opened(context):
    assert context.mock._opened is True


@then('The Mock is closed')
def step_mock_is_closed(context):
    assert context.mock._opened is False


@then('A correct record is saved')
def step_correct_record_saved(context):
    assert context._mainTableModel.rowCount() > 3, "{} is less than".format(
        context._mainTableModel.rowCount())
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
