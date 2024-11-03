from pytest_bdd import scenarios, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
import requests

scenarios("../features/categories/post_new_category.feature")

    
@when(parsers.parse('a new category is created with title "{title}" and description "{description}"'))
def post_new_category_all_parameter_fields_filled_out(title, description, returnedResponse):
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/categories', json={"title": title, "description": description})

@when(parsers.parse('a new category is created with title "{title}"'))
def post_new_category_only_title_field_filled_out(title, returnedResponse):
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/categories', json={"title": title})

@when(parsers.parse('a new category is created without a title and with only description "{description}"'))
def post_new_category_without_title(description, returnedResponse):
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/categories', json={"description": description})

@then(parsers.parse('the created category object with title "{title}" and description "{description}" shall be returned'))
def assert_category_object(title, description, returnedResponse):
    returnData = returnedResponse['response'].json()
    if (description == "empty"):
        description = ""
    assert returnData["title"] == title
    assert returnData["description"] == description
    delete_category_by_id(returnData["id"])