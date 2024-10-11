from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
import requests

# Normal Flow
@scenario("../features/projects/get_existing_tasks_of_existing_project.feature", "Get all tasks associated to an existing project")
def test_get_existing_tasks_of_existing_project():
    pass

# Alternate Flow
@scenario("../features/projects/get_existing_tasks_of_existing_project.feature", "Get all tasks associated to an existing project with a specific done status")
def test_get_existing_tasks_of_existing_project_with_done_status():
    pass

# Error Flow
@pytest.mark.expected_behaviour_failing
@scenario("../features/projects/get_existing_tasks_of_existing_project.feature", "Get all tasks associated to an invalid/non-existent project")
def test_get_tasks_of_non_existent_project():
    pass

@when(parsers.parse('the user requests to get all tasks associated to existing project with id "{projectId}"')) 
def get_existing_tasks_of_existing_project(projectId, returnedResponse):
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectIdToGetTasksOf = sortedProjects[int(projectId)]['id']
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/projects/{projectIdToGetTasksOf}/tasks')

@when(parsers.parse('the user requests to get all tasks associated to existing project with id "{projectId}" and done status "{doneStatus}"'))
def get_existing_tasks_of_existing_project_with_done_status(projectId, doneStatus, returnedResponse):
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectIdToGetTasksOf = sortedProjects[int(projectId)]['id']
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/projects/{projectIdToGetTasksOf}/tasks', params={"doneStatus": doneStatus})

@when(parsers.parse('the user requests to get all tasks associated to invalid project with id "{projectId}"'))
def get_tasks_of_non_existent_project(projectId, returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/projects/{projectId}/tasks')

@then(parsers.parse('a list of tasks associated to existing project with id "{projectId}" shall be returned and contain "{numberOfTasks}" tasks'))
def assert_tasks_returned(projectId, numberOfTasks, returnedResponse):
    returnData = returnedResponse['response'].json()
    assert len(returnData["todos"]) == int(numberOfTasks)
    # Assert that the returned tasks are associated to the correct project
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectIdToGetTasksOf = sortedProjects[int(projectId)]['id']
    for task in returnData["todos"]:
        assert task['tasksof'][0]['id'] == projectIdToGetTasksOf

@then(parsers.parse('a list of tasks associated to existing project with id "{projectId}" and with "{doneStatus}" doneStatus shall be returned and contain "{numberOfTasks}" tasks'))
def assert_tasks_returned_with_done_status(projectId, doneStatus, numberOfTasks, returnedResponse):
    returnData = returnedResponse['response'].json()
    assert len(returnData["todos"]) == int(numberOfTasks)
    # Assert that the returned tasks are associated to the correct project
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectIdToGetTasksOf = sortedProjects[int(projectId)]['id']
    # Assert that the returned tasks have the correct done status
    for task in returnData["todos"]:
        assert task['tasksof'][0]['id'] == projectIdToGetTasksOf
        assert task['doneStatus'] == doneStatus