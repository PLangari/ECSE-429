import requests
import pytest
from utils.default_variables import DEFAULT_API_URL
from utils.todos_utils import *

# HEAD Tests
def test_head_todos_with_existing_id():
    response = requests.head(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}/categories')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

@pytest.mark.actual_behaviour_passing
def test_head_todos_with_non_existing_id():
    nonexistent_id = 999
    response = requests.head(f'{DEFAULT_API_URL}/todos/{nonexistent_id}/categories')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

# OPTIONS Tests
def test_options_for_todos_with_existing_id():
    response = requests.options(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}/categories')
    assert response.status_code == 200
    assert response.headers["Allow"] == "OPTIONS, GET, HEAD, POST"

# GET Tests
def test_get_todo_categories_with_id():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_category(id_of_new_todo, default_category_id_1)
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories')
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["id"] == default_category_id_1
    assert response.json()["categories"][0]["title"] == default_category_name_1
    delete_todo_by_id(id_of_new_todo)

@pytest.mark.actual_behaviour_passing
def test_get_todo_categories_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.get(f'{DEFAULT_API_URL}/todos/{nonexistent_id}/categories')
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1

def test_get_todo_categories_of_todo_with_no_categories():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories')
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 0
    delete_todo_by_id(id_of_new_todo)

def test_get_todo_categories_with_id_by_title():
    # When category is linked to todo
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_category(id_of_new_todo, default_category_id_1)
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', params={"title": default_category_name_1})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["id"] == default_category_id_1
    assert response.json()["categories"][0]["title"] == default_category_name_1
    # When category is not linked to todo
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', params={"title": default_category_name_2})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 0
    delete_todo_by_id(id_of_new_todo)

def test_get_todo_categories_with_id_by_id():
    # When category is linked to todo
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_category(id_of_new_todo, default_category_id_1)
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', params={"id": default_category_id_1})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["id"] == default_category_id_1
    assert response.json()["categories"][0]["title"] == default_category_name_1
    # When category is not linked to todo
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', params={"id": default_category_id_2})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 0
    delete_todo_by_id(id_of_new_todo)

def test_get_todo_categories_with_id_by_description():
    # When category is linked to todo
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_category(id_of_new_todo, default_category_id_1)
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', params={"description": default_category_description_1})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["id"] == default_category_id_1
    assert response.json()["categories"][0]["title"] == default_category_name_1
    # When category is not linked to todo
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', params={"description": "super nice"})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 0
    delete_todo_by_id(id_of_new_todo)

# POST Tests
def test_post_todo_categories_with_id_and_category_id():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', json={"id": default_category_id_1})
    assert response.status_code == 201
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories')
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["id"] == default_category_id_1
    assert response.json()["categories"][0]["title"] == default_category_name_1
    assert response.json()["categories"][0]["description"] == default_category_description_1
    delete_todo_by_id(id_of_new_todo)

def test_post_todo_categories_with_id_and_nonexistent_category_id():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    nonexistent_id = 999
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', json={"id": nonexistent_id})
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == "Could not find thing matching value for id"
    delete_todo_by_id(id_of_new_todo)

@pytest.mark.actual_behaviour_passing
def test_post_todo_categories_with_id_and_category_name():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', json={"title": "New category"})
    assert response.status_code == 201
    assert response.json()["title"] == "New category"
    cat_id = response.json()["id"]
    
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories')
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["id"] == cat_id
    assert response.json()["categories"][0]["title"] == "New category"
    # Clean up
    delete_todo_by_id(id_of_new_todo)
    requests.delete(f'{DEFAULT_API_URL}/categories/{cat_id}')
    response = requests.get(f'{DEFAULT_API_URL}/categories/{cat_id}')
    assert response.status_code == 404

def test_post_todo_categories_with_id_and_no_cateogory_id_or_title():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', json={})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "title : field is mandatory"
    delete_todo_by_id(id_of_new_todo)


@pytest.mark.actual_behaviour_passing
def test_post_todo_categories_with_id_and_category_id_already_linked():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_category(id_of_new_todo, default_category_id_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/categories', json={"id": default_category_id_1})
    assert response.status_code == 201
    delete_todo_by_id(id_of_new_todo)


