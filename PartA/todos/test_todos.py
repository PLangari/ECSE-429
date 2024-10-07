import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.todos_utils import *
from setup import add_todos_to_database_and_cleanup

# OPTIONS Tests
def test_options_for_todos():
    response = requests.options(f'{DEFAULT_API_URL}/todos')
    assert response.status_code == 200
    assert response.headers["Allow"] == "OPTIONS, GET, HEAD, POST"

# HEAD Tests
def test_head_request_for_todos():
    response = requests.head(f'{DEFAULT_API_URL}/todos')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

# GET tests
def test_get_all_todos(add_todos_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/todos')
    assert response.status_code == 200
    assert len(response.json()['todos']) == 4

def test_get_all_done_todos(add_todos_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/todos', params={"doneStatus": "true"})
    assert response.status_code == 200
    assert len(response.json()['todos']) == 1
    assert response.json()['todos'][0]['title'] == new_todo_title_1
    assert response.json()['todos'][0]['description'] == new_todo_description_1

def test_get_all_not_done_todos(add_todos_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/todos', params={"doneStatus": "false"})
    assert response.status_code == 200
    assert len(response.json()['todos']) == 3
    response_sorted_by_id = sorted(response.json()['todos'], key=lambda x: int(x['id']))
    assert response_sorted_by_id[0]["title"] == default_todo_title_1
    assert response_sorted_by_id[1]["title"] == default_todo_title_2
    assert response_sorted_by_id[2]["title"] == new_todo_title_2

def test_get_all_todo_by_id(add_todos_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/todos', params={"id": "1"})
    assert response.status_code == 200
    assert len(response.json()['todos']) == 1
    assert response.json()["todos"][0]["title"] == default_todo_title_1

def test_get_all_todo_by_title(add_todos_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/todos', params={"title": new_todo_title_1})
    assert response.status_code == 200
    assert len(response.json()['todos']) == 1
    assert response.json()["todos"][0]["title"] == new_todo_title_1

def test_get_all_todo_by_description(add_todos_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/todos', params={"description": new_todo_description_2})
    assert response.status_code == 200
    assert len(response.json()['todos']) == 1
    assert response.json()["todos"][0]["title"] == new_todo_title_2

def test_get_all_todos_by_non_existing_id():
    response = requests.get(f'{DEFAULT_API_URL}/todos', params={"id": "100"})
    assert response.status_code == 200
    assert len(response.json()['todos']) == 0

# POST Tests
def test_post_new_todo_all_params():
    response = requests.post(f'{DEFAULT_API_URL}/todos', json={
        "title": "new task", 
        "doneStatus": False, 
        "description": "new descriptions for new task"
        })
    
    assert response.status_code == 201
    assert response.json()["title"] == "new task"
    assert response.json()["doneStatus"] == "false"
    assert response.json()["description"] == "new descriptions for new task"
    delete_todo_by_id(response.json()["id"])

def test_post_new_todo_only_title():
    response = requests.post(f'{DEFAULT_API_URL}/todos', json={"title": "new task"})
    assert response.status_code == 201
    assert response.json()["title"] == "new task"
    assert response.json()["doneStatus"] == "false"
    assert response.json()["description"] == ""

def test_post_new_todo_no_title():
    response = requests.post(f'{DEFAULT_API_URL}/todos', json={
        "doneStatus": False,
          "description": "new descriptions for new task"
          })
    assert response.status_code == 400

def test_post_new_todo_invalid_param():
    response = requests.post(f'{DEFAULT_API_URL}/todos', json={
        "title": "new task",
        "doneStatus": "false",
        "description": "new descriptions for new task"
        })
    assert response.status_code == 400


