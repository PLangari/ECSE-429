import requests
import pytest
from utils.default_variables import DEFAULT_API_URL
from utils.todos_utils import *

# OPTIONS Tests
def test_options_for_todos_with_existing_id():
    response = requests.options(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}/categories/{default_category_id_1}')
    assert response.status_code == 200
    assert response.headers["Allow"] == "OPTIONS, DELETE"

# DELETE Tests
def test_delete_todo_categories_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.delete(f'{DEFAULT_API_URL}/todos/{nonexistent_id}/categories/{default_category_id_1}')
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == 'Cannot invoke "uk.co.compendiumdev.thingifier.core.domain.instances.ThingInstance.getRelationships()" because "parent" is null'

def test_delete_todo_categories_with_nonexistent_category_id():
    nonexistent_category_id = 999
    response = requests.delete(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}/categories/{nonexistent_category_id}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find any instances with todos/{default_todo_id_1}/categories/{nonexistent_category_id}"

def test_delete_todo_categories_with_id_and_category_id_not_linked():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.delete(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories/{default_category_id_2}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find any instances with todos/{id_of_new_todo}/categories/{default_category_id_2}"
    delete_todo_by_id(id_of_new_todo)

def test_delete_todo_categories_with_valid_link():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_category(id_of_new_todo, default_category_id_1)
    response = requests.delete(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories/{default_category_id_1}')
    assert response.status_code == 200
    delete_todo_by_id(id_of_new_todo)

