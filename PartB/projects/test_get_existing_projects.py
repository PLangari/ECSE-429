from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
import requests

# Normal Flow
@scenario("../features/projects/get_existing_projects.feature", "Get all existing projects")
def test_get_existing_projects():
    pass

# Alternate Flow
@scenario("../features/projects/get_existing_projects.feature", "Get all existing projects by a specific active status")
def test_get_existing_projects_by_active_status():
    pass

# Error Flow
@pytest.mark.expected_behaviour_failing
@scenario("../features/projects/get_existing_projects.feature", "Get all existing projects by an invalid parameter")
def test_get_existing_projects_with_invalid_param():
    pass

@when("the user requests to get all existing projects")
def get_all_existing_projects(returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/projects')        # 4 created projects + 1 default project are in the database

@when(parsers.parse('the user requests to get all projects with active status of "{active}"'))
def get_all_projects_by_active_status(active, returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/projects', params={"active": active})

@when(parsers.parse('the user requests to get all existing projects with invalid parameter field owner "{owner}"'))
def get_all_projects_with_invalid_param(owner, returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/projects', params={"owner": owner})

@then("a list of existing projects shall be returned")
def assert_all_existing_projects(returnedResponse):
    returnData = returnedResponse['response'].json() 
    sortedProjects = sorted(returnData['projects'], key=lambda project: project['id'])
    assert len(sortedProjects) == 5
    assert sortedProjects[0]['title'] == "Office Work"
    assert sortedProjects[1]['title'] == "Yard Renovation"
    assert sortedProjects[2]['title'] == "Garage Cleanup"
    assert sortedProjects[3]['title'] == "Renovate Bathroom"
    assert sortedProjects[4]['title'] == "Clean Kitchen"

@then(parsers.parse('a list of existing projects with active status "{active}" shall be returned'))
def assert_all_projects_by_active_status(active, returnedResponse):
    returnData = returnedResponse['response'].json()
    sortedProjects = sorted(returnData['projects'], key=lambda project: project['id'])
    allTrueProjects = [project for project in sortedProjects if project['active'] == "true"]
    allFalseProjects = [project for project in sortedProjects if project['active'] == "false"]
    if active == "true":
        assert len(allTrueProjects) == 2
        assert allTrueProjects[0]['title'] == "Yard Renovation"
        assert allTrueProjects[1]['title'] == "Clean Kitchen"
    else:
        assert len(allFalseProjects) == 3
        assert allFalseProjects[0]['title'] == "Office Work"
        assert allFalseProjects[1]['title'] == "Garage Cleanup"
        assert allFalseProjects[2]['title'] == "Renovate Bathroom"

@then("an empty list with no projects shall be returned")
def assert_no_projects_returned(returnedResponse):
    returnData = returnedResponse['response'].json()
    assert len(returnData['projects']) == 0

