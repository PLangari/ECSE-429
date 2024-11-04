from pytest_bdd import scenario, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/categories/get_existing_todos_of_existing_category.feature", "Get all todos associated to an existing category")
def test_get_existing_todos_of_existing_category():
    pass

# Alternate Flow
@scenario("../features/categories/get_existing_todos_of_existing_category.feature", "Get all todos associated to an existing category with a specific done status")
def test_get_existing_todos_of_existing_category_with_done_status():
    pass

# Error Flow
@pytest.mark.expected_behaviour_failing
@scenario("../features/categories/get_existing_todos_of_existing_category.feature", "Get all todos associated to an invalid/non-existent category")
def test_get_todos_of_non_existent_category():
    pass

@when(parsers.parse('the user requests to get all todos associated to existing category with id "{categoryId}"')) 
def get_existing_todos_of_existing_category(categoryId, returnedResponse):
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    categoryIdToGetTodosOf = sortedCategories[int(categoryId)]['id']
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/categories/{categoryIdToGetTodosOf}/todos')

@when(parsers.parse('the user requests to get all todos associated to existing category with id "{categoryId}" and done status "{doneStatus}"'))
def get_existing_todos_of_existing_category_with_done_status(categoryId, doneStatus, returnedResponse):
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    categoryIdToGetTodosOf = sortedCategories[int(categoryId)]['id']
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/categories/{categoryIdToGetTodosOf}/todos', params={"doneStatus": doneStatus})

@when(parsers.parse('the user requests to get all todos associated to invalid category with id "{categoryId}"'))
def get_todos_of_non_existent_category(categoryId, returnedResponse):
    returnedResponse['response'] = requests.get(f'{DEFAULT_API_URL}/categories/{categoryId}/todos')

@then(parsers.parse('a list of todos associated to existing category with id "{categoryId}" shall be returned and contain "{numberOfTodos}" todos'))
def assert_todos_returned(categoryId, numberOfTodos, returnedResponse):
    returnData = returnedResponse['response'].json()
    assert len(returnData["todos"]) == int(numberOfTodos)
    # Get the category object
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories')
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    categoryToGetTodosOf = sortedCategories[int(categoryId)]
    # If there are no todos in the category, assert that the returned data does not contain todos
    if (int(numberOfTodos) == 0):
        assert 'todos' not in categoryToGetTodosOf
    else:
        # Get todo IDs in the category object's 'todos' field
        allTodoIDsOfCategory = [todo['id'] for todo in categoryToGetTodosOf['todos']]
        # Assert that the returned todos are in the correct category's 'todos' field
        for todo in returnData["todos"]:  
            assert todo['id'] in allTodoIDsOfCategory

@then(parsers.parse('a list of todos associated to existing category with id "{categoryId}" and with "{doneStatus}" doneStatus shall be returned and contain "{numberOfTodos}" todos'))
def assert_todos_returned_with_done_status(categoryId, doneStatus, numberOfTodos, returnedResponse):
    returnData = returnedResponse['response'].json()
    assert len(returnData["todos"]) == int(numberOfTodos)
    # Get the category object
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    categoryToGetTodosOf = sortedCategories[int(categoryId)]
    # If the returned data does not contain todos, assert that the category object does not have a 'todos' field
    if (int(numberOfTodos) == 0):
        assert 'todos' not in categoryToGetTodosOf
    else:
        # Get todo IDs in the category object's 'todos' field
        allTodoIDsOfCategory = [todo['id'] for todo in categoryToGetTodosOf['todos']]
        # Assert that the returned todos are in the correct category's 'todos' field and have the specified done status
        for todo in returnData["todos"]:  
            assert todo['id'] in allTodoIDsOfCategory
            assert todo['doneStatus'] == doneStatus