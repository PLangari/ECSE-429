import pytest
import requests
from pytest_bdd import given, then, parsers
from utils.default_variables import DEFAULT_API_URL

# Shared response fixture to hold the response object
@pytest.fixture
def returnedResponse():
    return {}

# Delete todo by ID. Used for test cleanup
def delete_todo_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/todos/{id}")
    assert response.status_code == 200

# Create a new todo with the given parameters
def create_new_todo(title, doneStatus, description):
    response = requests.post(DEFAULT_API_URL + "/todos", json={"title": title, "doneStatus": doneStatus, "description": description})
    assert response.status_code == 201
    return response.json()

# Delete project by ID. Used for test cleanup
def delete_project_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/projects/{id}")
    assert response.status_code == 200

# Create a new project with the given parameters
def create_new_project(title, completed, active, description):
    response = requests.post(DEFAULT_API_URL + "/projects", json={"title": title, "completed": completed, "active": active, "description": description})
    assert response.status_code == 201
    return response.json()

# Delete category by ID. Used for test cleanup
def delete_category_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/categories/{id}")
    assert response.status_code == 200

# Create a new category with the given parameters
def create_new_category(title, description):
    response = requests.post(DEFAULT_API_URL + "/categories", json={"title": title, "description": description})
    assert response.status_code == 201
    return response.json()

# Shared step definition to assert API responsiveness
@pytest.mark.order(1)
@given("the API is running and responsive")
def is_api_responsive():
    response = requests.get(DEFAULT_API_URL)
    assert response.status_code == 200, "API is not active"

# Add todos to the database and clean up after the tests
@given("the database contains existing todos")
def add_todos_to_database_and_cleanup():
    # Create todos
    todos = (
        create_new_todo("Buy groceries", False, "Buy milk, eggs, and bread"),
        create_new_todo("Do laundry", True, "Wash and fold clothes"),
        create_new_todo("Clean house", False, "Vacuum and mop floors"),
        create_new_todo("Water plants", True, "Water the plants in the garden")
    )
    yield 

    # Delete todos
    for todo in todos:
        delete_todo_by_id(todo['id'])

# Add projects to the database and clean up after the tests
@given("the database contains existing projects")
def add_projects_to_database_and_cleanup():
    # Create projects
    projects = (
        create_new_project("Yard Renovation", False, True, "Tidy up and freshen up the yard"),
        create_new_project("Garage Cleanup", True, False, "Tidy up and organize the garage"),
        create_new_project("Renovate Bathroom", False, False, "Needs a makeover"),
        create_new_project("Clean Kitchen", True, True, "Tidy up and clean the kitchen")
    )
    yield 
    # Delete projects
    for project in projects:
        delete_project_by_id(project['id'])

# Add categories to the database and clean up after the tests
@given("the database contains existing categories")
def add_categories_to_database_and_cleanup():
    # Create categories
    categories = (
        create_new_category("Home", "Tasks related to home"),
        create_new_category("Work", "Tasks related to work"),
        create_new_category("Personal", "Personal tasks"),
        create_new_category("School", "Tasks related to school")
    )
    yield 
    # Delete categories
    for category in categories:
        delete_category_by_id(category['id'])

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

