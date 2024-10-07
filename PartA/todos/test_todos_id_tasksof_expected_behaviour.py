import requests
import pytest
from utils.default_variables import DEFAULT_API_URL
from utils.todos_utils import *

@pytest.mark.expected_behaviour_failing
def test_head_todos_id_tasksof_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.head(f'{DEFAULT_API_URL}/todos/{nonexistent_id}/tasksof')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find an instance with todos/{nonexistent_id}"

@pytest.mark.expected_behaviour_failing
def test_get_for_todos_tasksof_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.get(f'{DEFAULT_API_URL}/todos/{nonexistent_id}/tasksof')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find an instance with todos/{nonexistent_id}"

@pytest.mark.expected_behaviour_failing
def test_post_todo_tasksof_with_id_and_project_name():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', json={"title": "Test Project"})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "Missing required field: id"
    delete_todo_by_id(id_of_new_todo)

@pytest.mark.expected_behaviour_failing
def test_post_todo_tasksof_with_id_and_no_project_id_or_name():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', json={})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "Missing required field: id"
    delete_todo_by_id(id_of_new_todo)

@pytest.mark.expected_behaviour_failing
def test_post_todo_tasksof_with_id_and_project_id_already_linked():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    add_todo_to_project(id_of_new_todo, default_project_id_1)
    response = requests.post(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}/tasksof', json={"id": default_project_id_1})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == f"Todo of id {id_of_new_todo} is already linked to category of id {default_category_id_1}"
    delete_todo_by_id(id_of_new_todo)