import requests
import pytest
from utils.default_variables import DEFAULT_API_URL
from utils.todos_utils import *

# HEAD Tests
def test_head_todos_id_tasksof_with_existing_id():
    response = requests.head(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}/tasksof')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

@pytest.mark.actual_behaviour_passing
def test_head_todos_id_tasksof_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.head(f'{DEFAULT_API_URL}/todos/{nonexistent_id}/tasksof')
    assert response.status_code == 200

# OPTIONS Tests
def test_options_for_todos_with_existing_id():
    response = requests.options(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}/tasksof')
    assert response.status_code == 200
    assert response.headers["Allow"] == "OPTIONS, GET, HEAD, POST"

# GET Tests
def test_get_for_todos_tasksof_with_existing_id():
    response = requests.get(f'{DEFAULT_API_URL}/todos/{default_todo_id_1}/tasksof')
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["id"] == default_project_id_1
    assert response.json()["projects"][0]["title"] == default_project_title_1

@pytest.mark.actual_behaviour_passing
def test_get_for_todos_tasksof_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.get(f'{DEFAULT_API_URL}/todos/{nonexistent_id}/tasksof')
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 2

def test_get_for_todos_tasksof_with_no_projects():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof')
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 0 

def test_get_for_todos_tasksof_with_id_by_id():
    p_id = requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "Test Project"}).json()["id"]
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_project(id_of_new_todo, p_id)

    # When project is linked to todo
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', params={"id": p_id})
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["id"] == p_id
    assert response.json()["projects"][0]["title"] == "Test Project"
    # When project is not linked to todo
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', params={"id": default_project_id_1})
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 0
    delete_todo_by_id(id_of_new_todo)
    requests.delete(f'{DEFAULT_API_URL}/projects/{p_id}')
    response = requests.get(f'{DEFAULT_API_URL}/projects/{p_id}')
    assert response.status_code == 404

def test_get_for_todos_tasksof_with_id_by_title():
    p_id = requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "Test Project"}).json()["id"]
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_project(id_of_new_todo, p_id)

    # When project is linked to todo
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', params={"title": "Test Project"})
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["id"] == p_id
    assert response.json()["projects"][0]["title"] == "Test Project"
    # When project is not linked to todo
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', params={"title": "Test Project 2"})
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 0
    delete_todo_by_id(id_of_new_todo)
    requests.delete(f'{DEFAULT_API_URL}/projects/{p_id}')
    response = requests.get(f'{DEFAULT_API_URL}/projects/{p_id}')
    assert response.status_code == 404

def test_get_for_todos_tasksof_with_id_by_description():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_project(id_of_new_todo, default_project_id_1)

    # When project is linked to todo
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', params={"description": ""})
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["id"] == default_project_id_1
    assert response.json()["projects"][0]["title"] == "Office Work"
    # When project is not linked to todo
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', params={"description": "Test Project Description 2"})
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 0
    delete_todo_by_id(id_of_new_todo)

# POST Tests
def test_post_for_todos_tasksof_with_id_and_project_id():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', json={"id": default_project_id_1})
    assert response.status_code == 201
    
    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof')
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["id"] == default_project_id_1
    assert response.json()["projects"][0]["title"] == default_project_title_1
    delete_todo_by_id(id_of_new_todo)

def test_post_for_todos_tasksof_with_id_and_nonexistent_project_id():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    nonexistent_id = 999
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', json={"id": nonexistent_id})
    assert response.status_code == 404
    print(response.json())
    assert response.json()["errorMessages"][0] == "Could not find thing matching value for id"
    delete_todo_by_id(id_of_new_todo)

@pytest.mark.actual_behaviour_passing
def test_post_todo_tasksof_with_id_and_project_name():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', json={"title": "Test Project"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Project"
    p_id = response.json()["id"]

    response = requests.get(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof')
    assert response.status_code == 200
    assert len(response.json()["projects"]) == 1
    assert response.json()["projects"][0]["id"] == p_id
    assert response.json()["projects"][0]["title"] == "Test Project"

    # Clean up
    delete_todo_by_id(id_of_new_todo)
    requests.delete(f'{DEFAULT_API_URL}/projects/{p_id}')
    response = requests.get(f'{DEFAULT_API_URL}/projects/{p_id}')
    assert response.status_code == 404

@pytest.mark.actual_behaviour_passing
def test_post_todo_tasksof_with_id_and_no_project_id_or_name():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', json={})
    assert response.status_code == 201
    p_id = response.json()["id"]
    
    delete_todo_by_id(id_of_new_todo)
    requests.delete(f'{DEFAULT_API_URL}/projects/{p_id}')
    response = requests.get(f'{DEFAULT_API_URL}/projects/{p_id}')
    assert response.status_code == 404

@pytest.mark.actual_behaviour_passing
def test_post_todo_tasksof_with_id_and_project_id_already_linked():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_project(id_of_new_todo, default_project_id_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', json={"id": default_project_id_1})
    assert response.status_code == 201
    delete_todo_by_id(id_of_new_todo)