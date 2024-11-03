from pytest_bdd import scenario, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/categories/get_existing_projects_of_existing_category.feature", "Get all projects associated to an existing category")
def test_get_existing_projects_of_existing_category():
    pass

# Alternate Flow
@scenario("../features/categories/get_existing_projects_of_existing_category.feature", "Get all projects associated to an existing category with a specific active status")
def test_get_existing_projects_of_existing_category_with_active_status():
    pass

# Error Flow
@pytest.mark.expected_behaviour_failing
@scenario("../features/categories/get_existing_projects_of_existing_category.feature", "Get all projects associated to an invalid/non-existent category")
def test_get_projects_of_non_existent_category():
    pass

@when(parsers.parse('the user requests to get all projects associated to existing category with id "{categoryId}"')) 
def get_existing_projects_of_existing_category(categoryId, returnedResponse):
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    categoryIdToGetProjectsOf = sortedCategories[int(categoryId)]['id']
    print("categoryIdToGetProjectsOf: ", categoryIdToGetProjectsOf)
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/categories/{categoryIdToGetProjectsOf}/projects')

@when(parsers.parse('the user requests to get all projects associated to existing category with id "{categoryId}" and active status "{active}"'))
def get_existing_projects_of_existing_category_with_active_status(categoryId, active, returnedResponse):
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    categoryIdToGetProjectsOf = sortedCategories[int(categoryId)]['id']
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/categories/{categoryIdToGetProjectsOf}/projects', params={"active": active})

@when(parsers.parse('the user requests to get all projects associated to invalid category with id "{categoryId}"'))
def get_projects_of_non_existent_category(categoryId, returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/categories/{categoryId}/projects')

@then(parsers.parse('a list of projects associated to existing category with id "{categoryId}" shall be returned and contain "{numberOfProjects}" projects'))
def assert_projects_returned(categoryId, numberOfProjects, returnedResponse):
    returnData = returnedResponse['response'].json()
    assert len(returnData["projects"]) == int(numberOfProjects)
    # Get the category object
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories')
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    categoryToGetProjectsOf = sortedCategories[int(categoryId)]
    # If there are no projects in the category, assert that the returned data does not contain projects
    if (int(numberOfProjects) == 0):
        assert 'projects' not in categoryToGetProjectsOf
    else:
        # Get project IDs in the category object's 'projects' field
        allProjectIDsOfCategory = [project['id'] for project in categoryToGetProjectsOf['projects']]
        # Assert that the returned projects are in the correct category's 'projects' field
        for project in returnData["projects"]:  
            assert project['id'] in allProjectIDsOfCategory

@then(parsers.parse('a list of projects associated to existing category with id "{categoryId}" and with "{active}" active status shall be returned and contain "{numberOfProjects}" projects'))
def assert_projects_returned_with_active_status(categoryId, active, numberOfProjects, returnedResponse):
    returnData = returnedResponse['response'].json()
    assert len(returnData["projects"]) == int(numberOfProjects)
    # Get the category object
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    categoryToGetProjectsOf = sortedCategories[int(categoryId)]
    # If the returned data does not contain projects, assert that the category object does not have a 'projects' field
    if (int(numberOfProjects) == 0):
        assert 'projects' not in categoryToGetProjectsOf
    else:
        # Get project IDs in the category object's 'projects' field
        allProjectIDsOfCategory = [project['id'] for project in categoryToGetProjectsOf['projects']]
        # Assert that the returned projects are in the correct category's 'projects' field and have the specified active status
        for project in returnData["projects"]:  
            assert project['id'] in allProjectIDsOfCategory
            assert project['active'] == active