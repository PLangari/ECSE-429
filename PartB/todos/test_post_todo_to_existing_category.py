from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/todos/post_todo_to_existing_category.feature", "Add an existing todo to an existing category")
def test_post_todo_to_existing_category():
    pass

# Alternate Flow
@scenario("../features/todos/post_todo_to_existing_category.feature", "Create a new category for the todo")
def test_post_todo_to_existing_category_with_only_title():
    pass

# Error Flow
@scenario("../features/todos/post_todo_to_existing_category.feature", "Add a todo to a nonexisting category")
def test_post_todo_to_existing_category_with_invalid_parameter():
    pass

@when(parsers.parse('the user requests to add an existing todo "{todoId}" to an existing category "{categoryId}"'))
def post_todo_to_existing_category(todoId, categoryId, returnedResponse):
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    cId = sortedCategories[int(categoryId)]['id']
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos')
    sortedTodos = sorted(allTodos.json()['todos'], key=lambda todo: todo['id'])
    tId = sortedTodos[int(todoId)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/todos/{tId}/categories', json={"id": cId})

@when(parsers.parse('the user requests to add an existing todo "{todoId}" to a new category "{categoryName}"'))
def post_todo_to_existing_category_with_only_title(todoId, categoryName, returnedResponse):
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos')
    sortedTodos = sorted(allTodos.json()['todos'], key=lambda todo: todo['id'])
    tId = sortedTodos[int(todoId)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/todos/{tId}/categories', json={"title": categoryName})

@when(parsers.parse('the user requests to add an existing todo "{todoId}" to a nonexisting category "{categoryId}"'))
def post_todo_to_existing_category_with_invalid_parameter(todoId, categoryId, returnedResponse):
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos')
    sortedTodos = sorted(allTodos.json()['todos'], key=lambda todo: todo['id'])
    tId = sortedTodos[int(todoId)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/todos/{tId}/categories', json={"id": categoryId})
    
@then(parsers.parse('the new category object "{categoryName}" shall be returned'))
def verify_new_category_with_only_title(categoryName, returnedResponse):
    returnData = returnedResponse["response"].json()
    assert returnData["title"] == categoryName
    delete_category_by_id(returnData['id'])