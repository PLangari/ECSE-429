import time
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.shared_step_definitions import *
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/interoperability/remove_todo_from_category.feature", "Remove an existing todo from a category")
def test_remove_todo_from_category():
    pass

# Alternate Flow (Expected to fail due to API issue)
@scenario("../features/interoperability/remove_todo_from_category.feature", "Remove an already removed todo from a category")
def test_remove_already_removed_todo_from_category():
    pass

# Error Flow
@scenario("../features/interoperability/remove_todo_from_category.feature", "Attempt to remove a non-existing todo from a category")
def test_remove_non_existing_todo_from_category():
    pass

@given("the database contains existing categories and todos")
def ensure_existing_categories_and_todos():
    # Setup a sample category and todo in the database
    requests.post(f'{DEFAULT_API_URL}/categories', json={"title": "Sample Category"})
    requests.post(f'{DEFAULT_API_URL}/todos', json={"title": "Sample Todo"})

@when(parsers.parse('the user requests to remove the todo with id "{todoId}" from category with id "{categoryId}"'))
@when(parsers.parse('the user requests to remove the todo with id "{todoId}" from category with id "{categoryId}" again'))
def remove_todo_from_category(todoId, categoryId, returnedResponse):
    # First, add the todo to the category to ensure it exists in the relationship
    requests.post(f'{DEFAULT_API_URL}/categories/{categoryId}/todos', json={"id": todoId})
    # Now, perform the DELETE request to remove the todo from the category
    returnedResponse['response'] = requests.delete(
        f'{DEFAULT_API_URL}/categories/{categoryId}/todos/{todoId}'
    )

@given(parsers.parse('the todo with id "{todoId}" is already removed from category with id "{categoryId}"'))
def ensure_todo_already_removed(todoId, categoryId):
    # Ensure the todo-category relationship is removed by attempting to delete it first
    requests.delete(f'{DEFAULT_API_URL}/categories/{categoryId}/todos/{todoId}')

@when(parsers.parse('the user requests to remove a non-existing todo with id "{todoId}" from category with id "{categoryId}"'))
def remove_non_existing_todo_from_category(todoId, categoryId, returnedResponse):
    # Perform the DELETE request with a non-existing todo or category ID
    returnedResponse['response'] = requests.delete(
        f'{DEFAULT_API_URL}/categories/{categoryId}/todos/{todoId}'
    )

@then(parsers.parse('a status code of "{statusCode}" shall be returned'))
def assert_status_code(statusCode, returnedResponse):
    response = returnedResponse['response']
    assert response.status_code == int(statusCode), f"Expected status code {statusCode}, but got {response.status_code}"

@then(parsers.parse('an error message "{errorMessage}" shall be returned'))
def assert_error_message(errorMessage, returnedResponse):
    response_data = returnedResponse['response'].json()
    actual_error_message = response_data.get("errorMessages", [""])[0]
    assert errorMessage in actual_error_message, f"Expected '{errorMessage}' but got '{actual_error_message}'"
