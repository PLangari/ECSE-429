import time
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/interoperability/manage_project_across_multiple_categories.feature", "Add a project to multiple categories")
def test_add_project_to_multiple_categories():
    pass

# Alternate Flow
@scenario("../features/interoperability/manage_project_across_multiple_categories.feature", "Remove a project from one category while it remains in another")
def test_remove_project_from_one_category():
    pass

# Error Flow
@scenario("../features/interoperability/manage_project_across_multiple_categories.feature", "Attempt to add a non-existing project to a category")
def test_add_non_existing_project_to_category():
    pass

@given("the database contains existing categories and projects")
def ensure_existing_categories_and_projects():
    # Setup a sample category and project in the database
    requests.post(f'{DEFAULT_API_URL}/categories', json={"title": "Sample Category"})
    requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "Sample Project"})
    time.sleep(1)

@when(parsers.parse('the user requests to add the project with id "{projectId}" to category with id "{categoryId}"'))
def add_project_to_category(projectId, categoryId, returnedResponse):
    # POST request to add project to category
    returnedResponse['response'] = requests.post(
        f'{DEFAULT_API_URL}/categories/{categoryId}/projects', json={"id": projectId}
    )

@given(parsers.parse('the project with id "{projectId}" is added to categories "{categoryId1}" and "{categoryId2}"'))
def ensure_project_added_to_multiple_categories(projectId, categoryId1, categoryId2):
    # Ensure the project is added to both categories
    requests.post(f'{DEFAULT_API_URL}/categories/{categoryId1}/projects', json={"id": projectId})
    requests.post(f'{DEFAULT_API_URL}/categories/{categoryId2}/projects', json={"id": projectId})
    time.sleep(1)

@when(parsers.parse('the user requests to remove the project with id "{projectId}" from category with id "{categoryId1}"'))
def remove_project_from_category(projectId, categoryId1, returnedResponse):
    # DELETE request to remove project from the first category
    returnedResponse['response'] = requests.delete(
        f'{DEFAULT_API_URL}/categories/{categoryId1}/projects/{projectId}'
    )

@then(parsers.parse('the project with id "{projectId}" shall still exist in category with id "{categoryId2}"'))
def verify_project_still_in_other_category(projectId, categoryId2):
    # Verify the project is still in the second category
    response = requests.get(f'{DEFAULT_API_URL}/categories/{categoryId2}/projects')
    projects = [project['id'] for project in response.json().get('projects', [])]
    assert projectId in projects, f"Expected project with id {projectId} to still be in category {categoryId2}"

@when(parsers.parse('the user requests to add a non-existing project with id "{projectId}" to category with id "{categoryId}"'))
def add_non_existing_project_to_category(projectId, categoryId, returnedResponse):
    # Attempt to add a non-existing project to a category
    returnedResponse['response'] = requests.post(
        f'{DEFAULT_API_URL}/categories/{categoryId}/projects', json={"id": projectId}
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
