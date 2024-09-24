import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.project_utils import *

# Setup/Teardown Methods
@pytest.fixture
def create_project_with_tasks():
    id_of_new_project = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    id_of_new_task_1 = add_task_to_project(id_of_new_project, new_task_1_title, new_task_1_doneStatus, new_task_1_description)
    id_of_new_task_2 = add_task_to_project(id_of_new_project, new_task_2_title, new_task_2_doneStatus, new_task_2_description)
    yield id_of_new_project, id_of_new_task_1, id_of_new_task_2
    delete_project_by_id(id_of_new_project)
    delete_task_by_id(id_of_new_task_1)
    delete_task_by_id(id_of_new_task_2)

# DELETE Tests
def test_delete_task_by_id_with_existing_id(create_project_with_tasks):
    id_of_new_project, id_of_new_task_1, id_of_new_task_2 = create_project_with_tasks
    # See tasks were added
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks")
    responseOrderedById=sorted(response.json()["todos"], key=lambda x: x["id"])
    assert response.status_code == 200
    assert len(responseOrderedById) == 2
    assert responseOrderedById[0]["id"] == str(id_of_new_task_1)
    assert responseOrderedById[0]["tasksof"][0]["id"] == str(id_of_new_project)
    assert responseOrderedById[1]["id"] == str(id_of_new_task_2)
    assert responseOrderedById[1]["tasksof"][0]["id"] == str(id_of_new_project)
    
    # Delete first task
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks/{id_of_new_task_1}")
    assert response.status_code == 200
    # Check if task was deleted
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks")
    assert len(response.json()["todos"]) == 1
    assert response.json()["todos"][0]["id"] == str(id_of_new_task_2)
    assert response.json()["todos"][0]["tasksof"][0]["id"] == str(id_of_new_project)
    
    # Delete second task
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks/{id_of_new_task_2}")
    assert response.status_code == 200
    # Check if task was deleted
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/tasks")
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 0

def test_delete_task_by_id_with_nonexistent_id():
    nonexisting_id = "999"
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{default_project_id}/tasks/{nonexisting_id}")
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find any instances with projects/{default_project_id}/tasks/{nonexisting_id}"
