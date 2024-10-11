from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
import requests

# Normal Flow
@scenario("../features/projects/post_new_task_to_existing_project.feature", "Create a new task for an existing project with all parameter fields filled out")
def test_post_new_task_to_existing_project():
    pass

# Alternate Flow
@scenario("../features/projects/post_new_task_to_existing_project.feature", "Create a new task for an existing project with all only the title parameter field filled out")
def test_post_new_task_to_existing_project_only_title_field_filled_out():
    pass

@scenario("../features/projects/post_new_task_to_existing_project.feature", "Create a new task for a project with an invalid/non-existent project id")
def test_post_new_task_to_non_existent_project():
    pass

@when(parsers.parse('the user requests to create a new task with title "{title}", done status "{doneStatus}", and description "{description}" for project with id "{projectId}"'))
def post_new_task_to_existing_project(title, doneStatus, description, projectId, returnedResponse):
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectIdToAddTaskTo = sortedProjects[int(projectId)]['id']
    doneStatusBoolean = doneStatus == "true"
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects/{projectIdToAddTaskTo}/tasks', json={"title": title, "doneStatus": doneStatusBoolean, "description": description})

@when(parsers.parse('the user requests to create a new task with title "{title}" for project with id "{projectId}"'))
def post_new_task_to_existing_project_only_title_field_filled_out(title, projectId, returnedResponse):
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectIdToAddTaskTo = sortedProjects[int(projectId)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects/{projectIdToAddTaskTo}/tasks', json={"title": title})

@when(parsers.parse('the user requests to create a new task with title "{title}", done status "{doneStatus}", and description "{description}" for project with invalid id "{projectId}"'))
def post_new_task_to_project_with_invalid_id(title, doneStatus, description, projectId, returnedResponse):
    doneStatusBoolean = doneStatus == "true"
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects/{projectId}/tasks', json={"title": title, "doneStatus": doneStatusBoolean, "description": description})


@then(parsers.parse('the created task object with title "{title}", done status "{doneStatus}", and description "{description}" for project with id "{projectId}" shall be returned'))
def assert_new_task_object(title, doneStatus, description, projectId, returnedResponse):
    if (description == "empty"):
        description = ""
    if (doneStatus == "empty"):
        doneStatus = "false"
    returnData = returnedResponse['response'].json()
    assert returnData["title"] == title
    assert returnData["doneStatus"] == doneStatus
    assert returnData["description"] == description
    projectIdTaskWasAddedTo = returnData["tasksof"][0]["id"]

    # Assert that the task is added to the correct project
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectWithTaskAdded = sortedProjects[int(projectId)]
    assert projectWithTaskAdded["id"] == projectIdTaskWasAddedTo

    # Delete task objects
    delete_task_by_id(returnData["id"])