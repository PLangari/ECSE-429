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

# Delete task by ID. Used for test cleanup
def delete_task_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/todos/{id}")
    assert response.status_code == 200

# Delete category by ID. Used for test cleanup
def delete_category_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/categories/{id}")
    assert response.status_code == 200

# Create a new project with the given parameters
def create_new_project(title, completed, active, description):
    response = requests.post(DEFAULT_API_URL + "/projects", json={"title": title, "completed": completed, "active": active, "description": description})
    assert response.status_code == 201
    return response.json()

def create_new_task(title, doneStatus, description, projectId):
    response = requests.post(DEFAULT_API_URL + f"/projects/{projectId}/tasks", json={"title": title, "doneStatus": doneStatus, "description": description})
    assert response.status_code == 201
    return response.json()

# Associate a task to a category
def link_task_to_category(taskId, categoryId):
    response = requests.post(DEFAULT_API_URL + f"/categories/{categoryId}/todos",  json={"id": taskId})
    assert response.status_code == 201

# Delete link between a task and a category
def delete_link_task_to_category(taskId, categoryId):
    response = requests.delete(DEFAULT_API_URL + f"/categories/{categoryId}/todos/{taskId}")
    assert response.status_code == 200

# Associate a project to a category
def link_project_to_category(projectId, categoryId):
    response = requests.post(DEFAULT_API_URL + f"/categories/{categoryId}/projects",  json={"id": projectId})
    assert response.status_code == 201

# Delete link between a project and a category
def delete_link_project_to_category(projectId, categoryId):
    response = requests.delete(DEFAULT_API_URL + f"/categories/{categoryId}/projects/{projectId}")
    assert response.status_code == 200

# Shared step definitio to assert API responsiveness
@pytest.mark.order(1)
@given("the API is running and responsive")
def is_api_responsive():
    response = requests.get(DEFAULT_API_URL)
    assert response.status_code == 200, "API is not active"

# Add projects to the database and clean up after the tests
@given("the database contains existing projects")
def add_projects_to_database_and_cleanup():
    # Create projects
    new_project_1 = create_new_project("Yard Renovation", False, True, "Tidy up and freshen up the yard")
    new_project_2 = create_new_project("Garage Cleanup", True, False, "Tidy up and organize the garage")
    new_project_3 = create_new_project("Renovate Bathroom", False, False, "Needs a makeover")
    new_project_4 = create_new_project("Clean Kitchen", True, True, "Tidy up and clean the kitchen")
    yield
    # Delete projects
    delete_project_by_id(new_project_1['id'])
    delete_project_by_id(new_project_2['id'])
    delete_project_by_id(new_project_3['id'])
    delete_project_by_id(new_project_4['id'])

# Add tasks to the database and clean up after the tests
@given("the database contains existing tasks associated to existing projects")
def add_tasks_associated_to_existing_projects_to_database_and_cleanup():
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects')
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    # IDs of projects to add tasks to
    projectId_1 = sortedProjects[1]['id']
    projectId_2 = sortedProjects[2]['id']
    # Add tasks to new_project_1
    new_task_1 = create_new_task("Mow Grass", False, "Take mower and cut grass short", projectId_1)
    new_task_2 = create_new_task("Plant Flowers", False, "Plant flowers in the garden", projectId_1)
     # Add tasks to new_project_2
    new_task_3 = create_new_task("Organize Tools", True, "Organize tools in the garage", projectId_2)
    new_task_4 = create_new_task("Throw Garbase", True, "Take cans out", projectId_2)
    new_task_5 = create_new_task("Clean Garage", False, "Sweep and clean the garage", projectId_2)
    yield
    # Delete tasks
    delete_task_by_id(new_task_1['id'])
    delete_task_by_id(new_task_2['id'])
    delete_task_by_id(new_task_3['id'])
    delete_task_by_id(new_task_4['id'])
    delete_task_by_id(new_task_5['id'])

# Associate tasks to existing categories and clean up after the tests
@given("the database contains existing todos associated to existing categories")
def add_tasks_associated_to_existing_categories_to_database_and_cleanup():
    # Get existing categories
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories')
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    # IDs of categories to add tasks to
    categoryId_1 = sortedCategories[2]['id']
    categoryId_2 = sortedCategories[3]['id']
    # Get existing tasks
    allTasks = requests.get(f'{DEFAULT_API_URL}/todos')
    sortedTasks = sorted(allTasks.json()['todos'], key=lambda task: task['id'])
    # IDs of tasks to add to categories
    taskId_1 = sortedTasks[2]['id']
    taskId_2 = sortedTasks[3]['id']
    taskId_3 = sortedTasks[4]['id']
    taskId_4 = sortedTasks[5]['id']
    # Add tasks to category_1
    link_task_to_category(taskId_1, categoryId_1)
    link_task_to_category(taskId_2, categoryId_1)
     # Add tasks to category_2
    link_task_to_category(taskId_3, categoryId_2)
    link_task_to_category(taskId_4, categoryId_2)
    yield
    # Delete links between tasks and categories
    delete_link_task_to_category(taskId_1, categoryId_1)
    delete_link_task_to_category(taskId_2, categoryId_1)
    delete_link_task_to_category(taskId_3, categoryId_2)
    delete_link_task_to_category(taskId_4, categoryId_2)
    
# Add projects associated to existing categories to the database and clean up after the tests
@given("the database contains existing projects associated to existing categories")
def add_projects_associated_to_existing_categories_to_database_and_cleanup():
    # Get existing categories
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories')
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    # IDs of categories to add projects to
    categoryId_1 = sortedCategories[2]['id']
    categoryId_2 = sortedCategories[3]['id']
    # Get existing projects
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects')
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    # IDs of projects to add to categories
    projectId_1 = sortedProjects[1]['id']
    projectId_2 = sortedProjects[2]['id']
    projectId_3 = sortedProjects[3]['id']
    projectId_4 = sortedProjects[4]['id']
    # Add projects to category_1
    link_project_to_category(projectId_1, categoryId_1)
    link_project_to_category(projectId_2, categoryId_1)
     # Add projects to category_2
    link_project_to_category(projectId_3, categoryId_2)
    link_project_to_category(projectId_4, categoryId_2)
    yield
    # Delete links between projects and categories
    delete_link_project_to_category(projectId_1, categoryId_1)
    delete_link_project_to_category(projectId_2, categoryId_1)
    delete_link_project_to_category(projectId_3, categoryId_2)
    delete_link_project_to_category(projectId_4, categoryId_2)

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