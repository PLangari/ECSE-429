from pytest_bdd import scenario, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/categories/edit_existing_category.feature", "Edit an existing category by modifying all fields")
def test_edit_existing_category_all_fields_modified():
    pass

# Alternate Flow
@scenario("../features/categories/edit_existing_category.feature", "Edit an existing category by modifying the title only")
def test_edit_existing_category_title_only():
    pass

# Error Flow
@scenario("../features/categories/edit_existing_category.feature", "Edit an existing category by providing an invalid field")
def test_edit_existing_category_with_invalid_param():
    pass

@when(parsers.parse('the user requests to edit an existing category with "{id}" with a new title "{title}" and description "{description}"'))
def edit_existing_category_all_fields_modified(id, title, description, returnedResponse):
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: int(category['id']))
    categoryIdToUpdate = sortedCategories[int(id)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/categories/{categoryIdToUpdate}', json={"title": title, "description": description})

@when(parsers.parse('the user requests to edit an existing category with "{id}" with a new title "{title}" only'))
def edit_existing_category_title_only(id, title, returnedResponse):
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: int(category['id']))
    categoryIdToUpdate = sortedCategories[int(id)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/categories/{categoryIdToUpdate}', json={"title": title})

@when(parsers.parse('the user requests to edit an existing category with "{id}" with an invalid parameter field "{owner}"'))
def edit_existing_category_with_invalid_param(id, owner, returnedResponse):
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: int(category['id']))
    categoryIdToUpdate = sortedCategories[int(id)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/categories/{categoryIdToUpdate}', json={"owner": owner})

@then(parsers.parse('the updated category object with title "{title}" and description "{description}" shall be returned'))
def assert_updated_category_object(title, description, returnedResponse):
    returnData = returnedResponse['response'].json()
    if (description == "empty"):
        description = ""
    assert returnData["title"] == title
    assert returnData["description"] == description