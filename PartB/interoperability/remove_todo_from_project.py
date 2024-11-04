from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/interoperability/remove_todo_from_project.feature", "Remove an existing todo from a project")
def test_remove_todo_from_project():
    pass

# Alternate Flow (Expected to use /todos/:id/tasksof/:id for the first delete and /projects/:id/tasks/:id for the second)
@pytest.mark.expected_behaviour_failing
@scenario("../features/interoperability/remove_todo_from_project.feature", "Remove an already removed todo from a project")
def test_remove_already_removed_todo_from_project():
    pass

# Error Flow
@scenario("../features/interoperability/remove_todo_from_project.feature", "Attempt to remove a non-existing todo from a project")
def test_remove_non_existing_todo_from_project():
    pass

@given("the database contains existing projects and todos")
def ensure_existing_projects_and_todos():
    # Setup a sample project and todo in the database
    requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "Sample Project"})
    requests.post(f'{DEFAULT_API_URL}/todos', json={"title": "Sample Todo"})

@when(parsers.parse('the user requests to remove the todo with id "{todoId}" from project with id "{projectId}"'))
def remove_todo_from_project(todoId, projectId, returnedResponse):
    # First, add the todo to the project to ensure it exists in the relationship
    requests.post(f'{DEFAULT_API_URL}/projects/{projectId}/tasks', json={"id": todoId})
    # Now, perform the DELETE request to remove the todo from the project
    returnedResponse['response'] = requests.delete(
        f'{DEFAULT_API_URL}/projects/{projectId}/tasks/{todoId}'
    )

@given(parsers.parse('the todo with id "{todoId}" is already removed from project with id "{projectId}" using /todos/:id/tasksof/:id'))
def ensure_todo_already_removed_alternate(todoId, projectId):
    # First, remove the relationship using the /todos/:id/tasksof/:id endpoint
    requests.delete(f'{DEFAULT_API_URL}/todos/{todoId}/tasksof/{projectId}')

@when(parsers.parse('the user requests to remove the todo with id "{todoId}" from project with id "{projectId}" again using /projects/:id/tasks/:id'))
def remove_todo_from_project_alternate(todoId, projectId, returnedResponse):
    # Perform the DELETE request using the /projects/:id/tasks/:id endpoint to remove the todo from the project
    returnedResponse['response'] = requests.delete(
        f'{DEFAULT_API_URL}/projects/{projectId}/tasks/{todoId}'
    )

@when(parsers.parse('the user requests to remove a non-existing todo with id "{todoId}" from project with id "{projectId}"'))
def remove_non_existing_todo_from_project(todoId, projectId, returnedResponse):
    # Perform the DELETE request with a non-existing todo or project ID
    returnedResponse['response'] = requests.delete(
        f'{DEFAULT_API_URL}/projects/{projectId}/tasks/{todoId}'
    )

@then(parsers.parse('a status code of "{statusCode}" shall be returned'))
def assert_status_code(statusCode, returnedResponse):
    response = returnedResponse['response']
    assert response.status_code == int(statusCode), f"Expected status code {statusCode}, but got {response.status_code}"

@then(parsers.parse('an error message "{errorMessage}" shall be returned'))
def assert_error_message(errorMessage, returnedResponse):
    response_data = returnedResponse['response'].json()
    actual_error_message = response_data.get("errorMessages", [""])[0]
    assert errorMessage in actual_error_message, f"Expected '{errorMessage}' but got '{actual_error_message}'"
