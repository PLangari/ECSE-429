import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.project_utils import *


# Setup/Teardown Methods
@pytest.fixture
def create_project_without_tasks():
    id_of_new_project = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    yield id_of_new_project
    delete_project_by_id(id_of_new_project)

@pytest.fixture
def create_project_with_tasks():
    id_of_new_project = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    id_of_new_task_1 = add_task_to_project(id_of_new_project, new_task_1_title, new_task_1_doneStatus, new_task_1_description)
    id_of_new_task_2 = add_task_to_project(id_of_new_project, new_task_2_title, new_task_2_doneStatus, new_task_2_description)
    yield id_of_new_project, id_of_new_task_1, id_of_new_task_2
    delete_project_by_id(id_of_new_project)
    delete_task_by_id(id_of_new_task_1)
    delete_task_by_id(id_of_new_task_2)

# GET Tests
def test_get_tasks_of_project_with_existing_id_and_existing_tasks(create_project_with_tasks):
    id_of_new_project, id_of_new_task_1, id_of_new_task_2 = create_project_with_tasks
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks")
    responseOrderedById=sorted(response.json()["todos"], key=lambda x: x["id"])
    assert response.status_code == 200
    assert len(responseOrderedById) == 2
    assert responseOrderedById[0]["id"] == str(id_of_new_task_1)
    assert responseOrderedById[0]["tasksof"][0]["id"] == str(id_of_new_project)
    assert responseOrderedById[1]["id"] == str(id_of_new_task_2)
    assert responseOrderedById[1]["tasksof"][0]["id"] == str(id_of_new_project)

def test_get_tasks_of_project_with_existing_id_and_no_tasks(create_project_without_tasks):
    id_of_new_project = create_project_without_tasks
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks")
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 0

@pytest.mark.actual_behaviour_working
def test_get_tasks_of_project_with_non_existing_id():
    nonexisting_id = "999"
    response = requests.get(f"{DEFAULT_API_URL}/projects/{nonexisting_id}/tasks")
    assert response.status_code == 200
    assert len(response.json()["todos"]) != 0
    assert response.json()["todos"][0]["tasksof"][0] != nonexisting_id

def test_get_tasks_of_project_with_existing_id_by_valid_title():
    response = requests.get(f'{DEFAULT_API_URL}/projects/{default_project_id}/tasks', params={"title": default_task_title})
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 1
    assert response.json()["todos"][0]["title"] == default_task_title
    assert response.json()["todos"][0]["tasksof"][0]["id"] == str(default_project_id)

def test_get_tasks_of_project_with_existing_id_by_valid_description():
    response = requests.get(f'{DEFAULT_API_URL}/projects/{default_project_id}/tasks', params={"description": default_task_description})
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 2

def test_get_tasks_of_project_with_existing_id_by_valid_doneStatus():
    response = requests.get(f'{DEFAULT_API_URL}/projects/{default_project_id}/tasks', params={"doneStatus": default_task_doneStatus})
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 2

def test_get_tasks_of_project_with_existing_id_by_nonexistent_title():
    response = requests.get(f'{DEFAULT_API_URL}/projects/{default_project_id}/tasks', params={"title": "Nonexistent"})
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 0

def test_get_tasks_of_project_with_existing_id_by_nonexistent_description():
    response = requests.get(f'{DEFAULT_API_URL}/projects/{default_project_id}/tasks', params={"description": "Nonexistent"})
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 0

def test_get_tasks_of_project_with_existing_id_by_nonexistent_doneStatus():
    response = requests.get(f'{DEFAULT_API_URL}/projects/{default_project_id}/tasks', params={"doneStatus": "true"})
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 0

# HEAD Tests
def test_head_projects_id_tasks():
    response = requests.head(f"{DEFAULT_API_URL}/projects/1/tasks")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

# POST Tests
def test_post_new_task_to_project_with_existing_id_and_all_fields_filled_out(create_project_without_tasks):
    id_of_new_project = create_project_without_tasks
    response = requests.post(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks", json={"title": new_task_1_title, "doneStatus": new_task_1_doneStatus, "description": new_task_1_description})
    assert response.status_code == 201
    assert response.json()["title"] == new_task_1_title
    assert response.json()["doneStatus"] == str(new_task_1_doneStatus).lower()
    assert response.json()["description"] == new_task_1_description
    assert response.json()["tasksof"][0]["id"] == str(id_of_new_project)
    delete_task_by_id(int(response.json()["id"]))

def test_post_new_task_to_project_with_non_existing_id():
    nonexisting_id = "999"
    response = requests.post(f"{DEFAULT_API_URL}/projects/{nonexisting_id}/tasks", json={"title": new_task_1_title, "doneStatus": new_task_1_doneStatus, "description": new_task_1_description})
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find parent thing for relationship projects/{nonexisting_id}/tasks"

def test_post_new_task_to_project_with_existing_id_and_invalid_field(create_project_without_tasks):
    invalid_field = "invalid"
    id_of_new_project = create_project_without_tasks
    response = requests.post(f'{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks', json={f"{invalid_field}": "Doesn't matter"})
    assert response.status_code == 400

def test_post_new_task_to_project_with_existing_id_and_no_title_filled_out(create_project_without_tasks):
    id_of_new_project = create_project_without_tasks
    response = requests.post(f'{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks', json={"doneStatus": new_task_1_doneStatus, "description": new_task_1_description})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "title : field is mandatory"

def test_post_new_task_to_project_with_existing_id_and_only_title_filled_out(create_project_without_tasks):
    id_of_new_project = create_project_without_tasks
    response = requests.post(f'{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks', json={"title": new_task_1_title})
    assert response.status_code == 201
    assert response.json()["title"] == new_task_1_title
    assert response.json()["doneStatus"] == "false"
    assert response.json()["description"] == ""
    assert response.json()["tasksof"][0]["id"] == str(id_of_new_project)
    delete_task_by_id(int(response.json()["id"]))


