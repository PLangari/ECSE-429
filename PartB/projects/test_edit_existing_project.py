from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
import requests

# Normal Flow
@scenario("../features/projects/edit_existing_project.feature", "Edit an existing project by modifying all fields")
def test_edit_existing_project_all_fields_modified():
    pass

# Alternate Flow
@scenario("../features/projects/edit_existing_project.feature", "Edit an existing project by modifying the title only")
def test_edit_existing_project_title_only():
    pass

# Error Flow
@scenario("../features/projects/edit_existing_project.feature", "Edit an existing project by providing an invalid field")
def test_edit_existing_project_with_invalid_param():
    pass

@when(parsers.parse('the user requests to edit an existing project with "{id}" with a new title "{title}", description "{description}", completed "{completed}", and active "{active}"'))
def edit_existing_project_all_fields_modified(id, title, description, completed, active, returnedResponse):
    completedBoolean = completed == "true"
    activeBoolean = active == "true"
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sorted_projects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectIdToUpdate = sorted_projects[int(id)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects/{projectIdToUpdate}', json={"title": title, "description": description, "completed": completedBoolean, "active": activeBoolean})

@when(parsers.parse('the user requests to edit an existing project with "{id}" with a new title "{title}" only'))
def edit_existing_project_title_only(id, title, returnedResponse):
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sorted_projects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectIdToUpdate = sorted_projects[int(id)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects/{projectIdToUpdate}', json={"title": title})

@when(parsers.parse('the user requests to edit an existing project with "{id}" with an invalid parameter field "{owner}"'))
def edit_existing_project_with_invalid_param(id, owner, returnedResponse):
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sorted_projects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    projectIdToUpdate = sorted_projects[int(id)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects/{projectIdToUpdate}', json={"owner": owner})

@then(parsers.parse('the updated project object with title "{title}", description "{description}", completed "{completed}", and active "{active}" shall be returned'))
def assert_updated_project_object(title, description, completed, active, returnedResponse):
    returnData = returnedResponse['response'].json()
    if (description == "empty"):
        description = ""
    assert returnData["title"] == title
    assert returnData["description"] == description
    assert returnData["completed"] == completed
    assert returnData["active"] == active