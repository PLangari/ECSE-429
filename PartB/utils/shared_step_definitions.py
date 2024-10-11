import pytest
import requests
from pytest_bdd import given, then, parsers
from utils.default_variables import DEFAULT_API_URL

# This file contains functions/step definitions that are shared across multiple test files

# Shared response fixture to hold the response object
@pytest.fixture
def returnedResponse():
    return {}

# Delete project by ID. Used for test cleanup
def delete_project_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/projects/{id}")
    assert response.status_code == 200

# Create a new project with the given parameters
def create_new_project(title, completed, active, description):
    response = requests.post(DEFAULT_API_URL + "/projects", json={"title": title, "completed": completed, "active": active, "description": description})
    assert response.status_code == 201
    return response.json()

# Shared step definitio to assert API responsiveness
@pytest.mark.order(1)
@given("the API is running and responsive")
def is_api_responsive():
    print("Checking if API is responsive")
    response = requests.get(DEFAULT_API_URL)
    assert response.status_code == 200, "API is not active"

# Add projects to the database and clean up after the tests
@given("the database contains existing projects")
def add_projects_to_database_and_cleanup():
    new_project_1 = create_new_project("Yard Renovation", False, True, "Tidy up and freshen up the yard")
    new_project_2 = create_new_project("Garage Cleanup", True, False, "Tidy up and organize the garage")
    new_project_3 = create_new_project("Renovate Bathroom", False, False, "Needs a makeover")
    new_project_4 = create_new_project("Clean Kitchen", True, True, "Tidy up and clean the kitchen")
    yield
    delete_project_by_id(new_project_1['id'])
    delete_project_by_id(new_project_2['id'])
    delete_project_by_id(new_project_3['id'])
    delete_project_by_id(new_project_4['id'])

# Shared step definition to assert the status code of the response
@then(parsers.parse('a status code of "{statusCode}" shall be returned'))
def assert_status_code_201(statusCode, returnedResponse):
    returnData = returnedResponse['response']
    assert returnData.status_code == int(statusCode)

# Shared step definition to assert the error message of the response
@then(parsers.parse('an error "{error}" shall be returned'))
def assert_error_message(error, returnedResponse):
    returnData = returnedResponse['response'].json()
    assert returnData["errorMessages"][0] == error