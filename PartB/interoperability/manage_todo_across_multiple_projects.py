import time
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/interoperability/manage_todo_across_multiple_projects.feature", "Add an existing todo to multiple projects")
def test_add_todo_to_multiple_projects():
    pass

# Alternate Flow (Expected to keep todo in one project after removal from another)
@scenario("../features/interoperability/manage_todo_across_multiple_projects.feature", "Remove a todo from one project while it remains in another")
def test_remove_todo_from_one_project_still_in_another():
    pass

# Error Flow
@scenario("../features/interoperability/manage_todo_across_multiple_projects.feature", "Attempt to add a non-existing todo to a project")
def test_add_non_existing_todo_to_project():
    pass

@given("the database contains existing projects and todos")
def setup_projects_and_todos():
    requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "Project A"})
    requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "Project B"})
    requests.post(f'{DEFAULT_API_URL}/todos', json={"title": "Sample Todo"})

@when(parsers.parse('the user adds the todo with id "{todoId}" to the project with id "{projectId}"'))
def add_todo_to_project(todoId, projectId, returnedResponse):
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects/{projectId}/tasks', json={"id": todoId})

@given(parsers.parse('the todo with id "{todoId}" is associated with the project with id "{projectId}"'))
def ensure_todo_in_project(todoId, projectId):
    requests.post(f'{DEFAULT_API_URL}/projects/{projectId}/tasks', json={"id": todoId})

@when(parsers.parse('the user requests to remove the todo with id "{todoId}" from project with id "{projectIdToRemove}"'))
def remove_todo_from_specific_project(todoId, projectIdToRemove, returnedResponse):
    returnedResponse['response'] = requests.delete(f'{DEFAULT_API_URL}/projects/{projectIdToRemove}/tasks/{todoId}')

@then(parsers.parse('the todo with id "{todoId}" should still be associated with project with id "{remainingProjectId}"'))
def assert_todo_still_in_project(todoId, remainingProjectId):
    response = requests.get(f'{DEFAULT_API_URL}/projects/{remainingProjectId}/tasks')
    response_data = response.json()
    # Handle both string and integer IDs in case of type mismatch
    todo_ids = [str(task['id']) for task in response_data.get('todos', [])]
    assert str(todoId) in todo_ids, f"Expected todo with ID {todoId} to still be in project {remainingProjectId}, but it was not found."

@when(parsers.parse('the user tries to add a non-existing todo with id "{invalidTodoId}" to project with id "{projectId}"'))
def add_non_existing_todo_to_project(invalidTodoId, projectId, returnedResponse):
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects/{projectId}/tasks', json={"id": invalidTodoId})

@then(parsers.parse('a status code of "{statusCode}" shall be returned'))
def assert_status_code(statusCode, returnedResponse):
    response = returnedResponse['response']
    assert response.status_code == int(statusCode), f"Expected status code {statusCode}, but got {response.status_code}"

@then(parsers.parse('an error message "{errorMessage}" shall be returned'))
def assert_error_message(errorMessage, returnedResponse):
    response_data = returnedResponse['response'].json()
    actual_error_message = response_data.get("errorMessages", [""])[0]
    assert errorMessage in actual_error_message, f"Expected '{errorMessage}' but got '{actual_error_message}'"
