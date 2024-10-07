import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.todos_utils import *

# HEAD Tests
def test_head_todos_with_existing_id():
    response = requests.head(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

def test_head_todos_with_non_existing_id():
    nonexistent_id = 999
    response = requests.head(f'{DEFAULT_API_URL}/todos/{nonexistent_id}')
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"

# OPTIONS Tests
def test_options_for_todos_with_existing_id():
    response = requests.options(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}')
    assert response.status_code == 200
    assert response.headers["Allow"] == "OPTIONS, GET, HEAD, POST, PUT, DELETE"

# GET Tests
def test_get_todo_by_existing_id():
    response = requests.get(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}')
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 1
    assert response.json()["todos"][0]["title"] == default_todo_title_1

def test_get_todo_by_non_existing_id():
    nonexistent_id = 999
    response = requests.get(f'{DEFAULT_API_URL}/todos/{nonexistent_id}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find an instance with todos/{nonexistent_id}"

# POST Tests
def test_post_todo_with_id_and_all_fields_filled_out():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}', json={"title": new_todo_title_2, "doneStatus": new_todo_doneStatus_2, "description": new_todo_description_2})
    assert response.status_code == 200
    assert response.json()["title"] == new_todo_title_2
    assert response.json()["doneStatus"] == new_todo_doneStatus_return_2
    assert response.json()["description"] == new_todo_description_2
    delete_todo_by_id(id_of_new_todo_1)

def test_post_todo_with_id_and_no_fields_filled_out():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}', json={})
    assert response.status_code == 200
    assert response.json()["title"] == new_todo_title_1
    assert response.json()["doneStatus"] == new_todo_doneStatus_return_1
    assert response.json()["description"] == new_todo_description_1
    delete_todo_by_id(id_of_new_todo_1)

def test_post_todo_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.post(f'{DEFAULT_API_URL}/todos/{nonexistent_id}', json={"title": new_todo_title_2, "doneStatus": new_todo_doneStatus_2, "description": new_todo_description_2})
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"No such todo entity instance with GUID or ID {nonexistent_id} found"

def test_post_todo_with_id_and_invalid_fields():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}', json={"title": new_todo_title_2, "doneStatus": "invalid", "description": new_todo_description_2})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "Failed Validation: doneStatus should be BOOLEAN"
    delete_todo_by_id(id_of_new_todo_1)

# PUT Tests
def test_put_todo_with_existing_id_and_all_fields_filled_out():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.put(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}', json={"title": new_todo_title_2, "doneStatus": new_todo_doneStatus_2, "description": new_todo_description_2})
    assert response.status_code == 200
    assert response.json()["title"] == new_todo_title_2
    assert response.json()["doneStatus"] == new_todo_doneStatus_return_2
    assert response.json()["description"] == new_todo_description_2
    delete_todo_by_id(id_of_new_todo_1)

def test_put_todo_with_existing_id_and_no_fields_filled_out():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.put(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}', json={})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "title : field is mandatory"
    delete_todo_by_id(id_of_new_todo_1)

def test_put_todo_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.put(f'{DEFAULT_API_URL}/todos/{nonexistent_id}', json={"title": new_todo_title_2, "doneStatus": new_todo_doneStatus_2, "description": new_todo_description_2})
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Invalid GUID for {nonexistent_id} entity todo"

def test_put_todo_with_existing_id_and_invalid_fields():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.put(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}', json={"title": new_todo_title_2, "doneStatus": "invalid", "description": new_todo_description_2})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "Failed Validation: doneStatus should be BOOLEAN"
    delete_todo_by_id(id_of_new_todo_1)

@pytest.mark.actual_behaviour_passing
def test_put_todo_with_id_and_only_description_filled_out():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.put(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}', json={"description": new_todo_description_2})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "title : field is mandatory"
    delete_todo_by_id(id_of_new_todo_1)

@pytest.mark.actual_behaviour_passing
def test_put_todo_with_id_and_only_doneStatus_filled_out():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.put(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}', json={"doneStatus": new_todo_doneStatus_2})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "title : field is mandatory"
    delete_todo_by_id(id_of_new_todo_1)

# DELETE Tests
def test_delete_todo_with_existing_id():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.delete(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}')
    assert response.status_code == 200
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find an instance with todos/{id_of_new_todo_1}"

def test_delete_todo_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.delete(f'{DEFAULT_API_URL}/todos/{nonexistent_id}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find any instances with todos/{nonexistent_id}"

    