import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.project_utils import *

# HEAD Tests
def test_head_projects_with_existing_id():
    response = requests.head(f'{DEFAULT_API_URL}/projects/{default_project_id}')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

def test_head_projects_with_non_existing_id():
    nonexistent_id = 999
    response = requests.head(f'{DEFAULT_API_URL}/projects/{nonexistent_id}')
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"

# OPTIONS Tests

def test_options_for_projects_with_existing_id():
    response = requests.options(f'{DEFAULT_API_URL}/projects/{default_project_id}')
    assert response.status_code == 200
    assert response.headers["Allow"] == "OPTIONS, GET, HEAD, POST, PUT, DELETE"

# GET Tests
def test_get_project_by_existing_id():
    response = requests.get(f'{DEFAULT_API_URL}/projects/{default_project_id}')
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["title"] == default_project_title

def test_get_project_by_non_existing_id():
    nonexistent_id = 999
    response = requests.get(f'{DEFAULT_API_URL}/projects/{nonexistent_id}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find an instance with projects/{nonexistent_id}"

#POST Tests
def test_post_project_with_id_and_all_fields_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.post(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"title": new_project_2_title, "completed": new_project_2_completed, "active": new_project_2_active, "description": new_project_2_description})
    assert response.status_code == 200
    assert response.json()["title"] == new_project_2_title
    assert response.json()["completed"] == "true"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == new_project_2_description
    delete_project_by_id(id_of_new_project_1)

def test_post_project_with_id_and_no_fields_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.post(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={})
    assert response.status_code == 200
    assert response.json()["title"] == new_project_1_title
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "true"
    assert response.json()["description"] == new_project_1_description
    delete_project_by_id(id_of_new_project_1)

def test_post_project_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.post(f'{DEFAULT_API_URL}/projects/{nonexistent_id}', json={"title": new_project_2_title, "completed": new_project_2_completed, "active": new_project_2_active, "description": new_project_2_description})
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"No such project entity instance with GUID or ID {nonexistent_id} found"

def test_post_project_with_id_and_bad_field():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    invalid_field = "invalid_field"
    response = requests.post(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={f"{invalid_field}": "Doesn't matter"})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == f"Could not find field: {invalid_field}"
    delete_project_by_id(id_of_new_project_1)

# PUT Tests
def test_put_project_with_id_and_all_fields_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"title": new_project_2_title, "completed": new_project_2_completed, "active": new_project_2_active, "description": new_project_2_description})
    assert response.status_code == 200
    assert response.json()["title"] == new_project_2_title
    assert response.json()["completed"] == "true"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == new_project_2_description
    delete_project_by_id(id_of_new_project_1)

def test_put_project_with_id_and_no_fields_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={})
    assert response.status_code == 200
    assert response.json()["title"] == ""
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == ""
    delete_project_by_id(id_of_new_project_1)

@pytest.mark.actual_behaviour_passing
def test_put_project_with_id_and_only_title_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"title": new_project_2_title})
    assert response.status_code == 200
    assert response.json()["title"] == new_project_2_title
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == ""
    delete_project_by_id(id_of_new_project_1)

@pytest.mark.actual_behaviour_passing
def test_put_project_with_id_and_only_description_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"description": new_project_2_description})
    assert response.status_code == 200
    assert response.json()["title"] == ""
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == new_project_2_description
    delete_project_by_id(id_of_new_project_1)

@pytest.mark.actual_behaviour_passing
def test_put_with_id_and_only_completed_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == ""
    assert response.json()["completed"] == "true"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == ""
    delete_project_by_id(id_of_new_project_1)

@pytest.mark.actual_behaviour_passing
def test_put_with_id_and_only_active_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"active": False})
    assert response.status_code == 200
    assert response.json()["title"] == ""
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == ""
    delete_project_by_id(id_of_new_project_1)

def test_put_project_with_id_and_bad_field():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    invalid_field = "invalid_field"
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={f"{invalid_field}": "Doesn't matter"})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == f"Could not find field: {invalid_field}"
    delete_project_by_id(id_of_new_project_1)

# DELETE Tests
def test_delete_project_with_existing_id():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.delete(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}')
    assert response.status_code == 200
    response = requests.get(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find an instance with projects/{id_of_new_project_1}"

def test_delete_project_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.delete(f'{DEFAULT_API_URL}/projects/{nonexistent_id}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find any instances with projects/{nonexistent_id}"

