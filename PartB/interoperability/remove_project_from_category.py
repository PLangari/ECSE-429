import time
from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/interoperability/remove_project_from_category.feature", "Remove an existing project from a category")
def test_remove_project_from_category():
    pass

# Alternate Flow
@scenario("../features/interoperability/remove_project_from_category.feature", "Remove an already removed project from a category")
def test_remove_already_removed_project_from_category():
    pass

# Error Flow
@scenario("../features/interoperability/remove_project_from_category.feature", "Attempt to remove a non-existing project from a category")
def test_remove_non_existing_project_from_category():
    pass

@when(parsers.parse('the user requests to remove the project with id "{projectId}" from category with id "{categoryId}"'))
@when(parsers.parse('the user requests to remove the project with id "{projectId}" from category with id "{categoryId}" again'))
def remove_project_from_category(projectId, categoryId, returnedResponse):
    # First, add the project to the category to ensure it exists in the relationship
    requests.post(f'{DEFAULT_API_URL}/categories/{categoryId}/projects', json={"id": projectId})
    # Now, perform the DELETE request to remove the project from the category
    returnedResponse['response'] = requests.delete(
        f'{DEFAULT_API_URL}/categories/{categoryId}/projects/{projectId}'
    )

@given(parsers.parse('the project with id "{projectId}" is already removed from category with id "{categoryId}"'))
def ensure_project_already_removed(projectId, categoryId):
    # Ensure the project-category relationship is removed by attempting to delete it first
    requests.delete(f'{DEFAULT_API_URL}/categories/{categoryId}/projects/{projectId}')
    time.sleep(1)  # Allow API to process the delete

@when(parsers.parse('the user requests to remove a non-existing project with id "{projectId}" from category with id "{categoryId}"'))
def remove_non_existing_project_from_category(projectId, categoryId, returnedResponse):
    # Perform the DELETE request with a non-existing project or category ID
    returnedResponse['response'] = requests.delete(
        f'{DEFAULT_API_URL}/categories/{categoryId}/projects/{projectId}'
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
