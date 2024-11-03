from pytest_bdd import scenario, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/categories/get_existing_categories.feature", "Get all existing categories")
def test_get_existing_categories():
    pass

# Alternate Flow
@scenario("../features/categories/get_existing_categories.feature", "Get all existing categories by a specific title")
def test_get_existing_categories_by_title():
    pass

# Error Flow
@pytest.mark.expected_behaviour_failing
@scenario("../features/categories/get_existing_categories.feature", "Get all existing categories by an invalid parameter")
def test_get_existing_categories_with_invalid_param():
    pass

@when("the user requests to get all existing categories")
def get_all_existing_categories(returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/categories')        # 4 created categories + 1 default category are in the database

@when(parsers.parse('the user requests to get all categories with title "{title}"'))
def get_all_categories_by_title(title, returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/categories', params={"title": title})

@when(parsers.parse('the user requests to get all existing categories with invalid parameter field owner "{owner}"'))
def get_all_categories_with_invalid_param(owner, returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/categories', params={"owner": owner})

@then("a list of existing categories shall be returned")
def assert_all_existing_categories(returnedResponse):
    returnData = returnedResponse['response'].json()
    sortedCategories = sorted(returnData['categories'], key=lambda category: int(category['id']))
    print("sortedCategories: ", sortedCategories)
    assert len(sortedCategories) == 6
    assert sortedCategories[0]['title'] == "Office"
    assert sortedCategories[1]['title'] == "Home"
    assert sortedCategories[2]['title'] == "Home"
    assert sortedCategories[3]['title'] == "Work"
    assert sortedCategories[4]['title'] == "Personal"
    assert sortedCategories[5]['title'] == "School"

@then(parsers.parse('a list of existing categories with title "{title}" shall be returned'))
def assert_all_categories_by_title(title, returnedResponse):
    returnData = returnedResponse['response'].json()
    categories = returnData['categories']
    assert len(categories) == 1
    assert categories[0]['title'] == title

@then("an empty list with no categories shall be returned")
def assert_no_categories_returned(returnedResponse):
    returnData = returnedResponse['response'].json()
    assert len(returnData['categories']) == 0

