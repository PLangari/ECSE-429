from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/todos/edit_existing_todo.feature", "Edit an existing todo by modifying all fields")
def test_edit_existing_todo_all_fields_modified():
    pass

# Alternate Flow
@scenario("../features/todos/edit_existing_todo.feature", "Edit an existing todo by modifying the title only")
def test_edit_existing_todo_title_only():
    pass

# Error Flow
@scenario("../features/todos/edit_existing_todo.feature", "Edit an existing todo by providing an invalid field")
def test_edit_existing_todo_with_invalid_param():
    pass

@when(parsers.parse('the user requests to edit an existing todo with "{id}" with a new title "{title}", description "{description}", doneStatus "{doneStatus}"'))
def edit_existing_todo_all_fields_modified(id, title, description, doneStatus, returnedResponse):
    print(id)
    doneStatusBoolean = doneStatus == "true"
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos')
    sortedTodos = sorted(allTodos.json()['todos'], key=lambda todo: todo['id'])
    todoIdToUpdate = sortedTodos[int(id)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/todos/{todoIdToUpdate}', json={"title": title, "description": description, "doneStatus": doneStatusBoolean})

@when(parsers.parse('the user requests to edit an existing todo with "{id}" with a new title "{title}" only'))
def edit_existing_todo_title_only(id, title, returnedResponse):
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos') 
    sortedTodos = sorted(allTodos.json()['todos'], key=lambda todo: todo['id'])
    todoIdToUpdate = sortedTodos[int(id)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/todos/{todoIdToUpdate}', json={"title": title})

@when(parsers.parse('the user requests to edit an existing todo with "{id}" with an invalid parameter field "{owner}"'))
def edit_existing_todo_with_invalid_param(id, owner, returnedResponse):
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos') 
    sortedTodos = sorted(allTodos.json()['todos'], key=lambda todo: todo['id'])
    todoIdToUpdate = sortedTodos[int(id)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/todos/{todoIdToUpdate}', json={"owner": owner})

@then(parsers.parse('the updated todo object with title "{title}", description "{description}", and doneStatus "{doneStatus}" shall be returned'))
def assert_edited_todo_object(title, description, doneStatus, returnedResponse):
    returnData = returnedResponse['response'].json()
    if (description == "empty"):
        description = returnData["description"]
    if (doneStatus == "empty"):
        doneStatus = returnData["doneStatus"]
    print(returnedResponse)
    assert returnData["title"] == title
    assert returnData["description"] == description
    assert returnData["doneStatus"] == doneStatus


