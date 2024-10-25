from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/todos/get_existing_todos.feature", "Get all existing todos")
def test_get_existing_todos():
    pass

# Alternate Flow
@scenario("../features/todos/get_existing_todos.feature", "Get all existing todos by a specific doneStatus")
def test_get_existing_todos_by_done_status():
    pass

# Error Flow
@pytest.mark.expected_behaviour_failing
@scenario("../features/todos/get_existing_todos.feature", "Get all existing todos by an invalid parameter")
def test_get_existing_todos_with_invalid_parameter():
    pass

@when(parsers.parse('the user requests to get all existing todos'))
def get_all_existing_todos(returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/todos')

@when(parsers.parse('the user requests to get all existing todos with doneStatus "{doneStatus}"'))
def get_all_existing_todos_by_done_status(doneStatus, returnedResponse):
    doneStatusBoolean = doneStatus == "true"
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/todos?doneStatus={doneStatusBoolean}')

@when(parsers.parse('the user requests to get all existing todos with an invalid parameter field owner "{owner}"'))
def get_existing_todos_with_invalid_parameter(owner, returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/todos?owner={owner}')

@then(parsers.parse('the list of all existing todos shall be returned'))
def assert_all_existing_todos(returnedResponse):
    assert returnedResponse['response'].status_code == 200
    assert len(returnedResponse['response'].json()['todos']) > 0

@then(parsers.parse('a list of all existing todos with doneStatus "{doneStatus}" shall be returned'))
def assert_all_existing_todos_by_done_status(doneStatus, returnedResponse):
    doneStatusBoolean = doneStatus == "true"
    allTodos = returnedResponse['response'].json()['todos']
    for todo in allTodos:
        assert todo['doneStatus'] == doneStatusBoolean
    