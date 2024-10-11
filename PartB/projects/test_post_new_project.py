from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
import requests

# Normal Flow
@scenario("../features/projects/post_new_project.feature", "Post a new project with all parameter fields filled out")
def test_post_new_project_all_parameter_fields_filled_out():
    pass

# Alternate Flow
@scenario("../features/projects/post_new_project.feature", "Post a new project with only title field filled out")
def test_post_new_project_only_title_field_filled_out():
    pass

# Error Flow
@scenario("../features/projects/post_new_project.feature", "Post a new project with an invalid parameter field")
def test_post_new_project_with_invalid_param():
    pass

@when(parsers.parse('the user wants to post a new project with title "{title}", description "{description}", completed "{completed}", and active "{active}"'))
def post_new_project_all_parameter_fields_filled_out(title, description, completed, active, returnedResponse):
    completedBoolean = completed == "true"
    activeBoolean = active == "true"
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects', json={"title": title, "description": description, "completed": completedBoolean, "active": activeBoolean})

@when(parsers.parse('the user wants to post a new project with title "{title}"'))
def post_new_project_only_title_field_filled_out(title, returnedResponse):
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects', json={"title": title})

@when(parsers.parse('the user wants to post a new project with invalid field owner "{owner}"'))
def post_new_project_with_invalid_param(owner, returnedResponse):
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/projects', json={"owner": owner})

@then(parsers.parse('the created project object with title "{title}", description "{description}", completed "{completed}", and active "{active}" shall be returned'))
def assert_project_object(title, description, completed, active, returnedResponse):
    returnData = returnedResponse['response'].json()
    if (description == "empty"):
        description = ""
    assert returnData["title"] == title
    assert returnData["description"] == description
    assert returnData["completed"] == completed
    assert returnData["active"] == active
    delete_project_by_id(returnData["id"])









