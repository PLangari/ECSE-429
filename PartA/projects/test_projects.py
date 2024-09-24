import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.project_utils import *

# Setup
@pytest.fixture
def add_projects_to_database_and_cleanup():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    id_of_new_project_2 = create_new_project(new_project_2_title, new_project_2_completed, new_project_2_active, new_project_2_description)
    yield
    delete_project_by_id(id_of_new_project_1)
    delete_project_by_id(id_of_new_project_2)

# OPTIONS Tests
def test_options_for_projects():
    response = requests.options(f'{DEFAULT_API_URL}/projects')
    assert response.status_code == 200
    assert response.headers["Allow"] == "OPTIONS, GET, HEAD, POST"

# GET Tests

def test_get_all_projects(add_projects_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/projects')
    assert response.status_code == 200
    assert len(response.json()['projects']) == 3

def test_get_all_active_projects(add_projects_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/projects', params={"active": "true"})
    assert response.status_code == 200
    assert len(response.json()['projects']) == 1
    assert response.json()['projects'][0]['title'] == new_project_1_title
    assert response.json()['projects'][0]['description'] == new_project_1_description

def test_get_all_inactive_projects(add_projects_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/projects', params={"active": "false"})
    assert response.status_code == 200
    assert len(response.json()['projects']) == 2
    response_sorted_by_id = sorted(response.json()['projects'], key=lambda x: int(x['id']))
    assert response_sorted_by_id[0]["title"] == default_project_title
    assert response_sorted_by_id[1]["title"] == new_project_2_title

def test_get_all_completed_projects(add_projects_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/projects', params={"completed": "true"})
    assert response.status_code == 200
    assert len(response.json()['projects']) == 1
    assert response.json()['projects'][0]['title'] == new_project_2_title
    assert response.json()['projects'][0]['description'] == new_project_2_description

def test_get_all_incompleted_projects(add_projects_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/projects', params={"completed": "false"})
    assert response.status_code == 200
    assert len(response.json()['projects']) == 2
    response_sorted_by_id = sorted(response.json()['projects'], key=lambda x: int(x['id']))
    assert response_sorted_by_id[0]["title"] == default_project_title
    assert response_sorted_by_id[1]["title"]  == new_project_1_title

def test_get_all_projects_by_existing_id():
    response = requests.get(f'{DEFAULT_API_URL}/projects', params={"id": "1"})
    assert response.status_code == 200
    assert len(response.json()['projects']) == 1
    assert response.json()['projects'][0]['title'] == default_project_title
    assert response.json()['projects'][0]['description'] == default_project_description

def test_get_all_projects_by_existing_title(add_projects_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/projects', params={"title": new_project_1_title})
    assert response.status_code == 200
    assert len(response.json()['projects']) == 1
    assert response.json()['projects'][0]['title'] == new_project_1_title
    assert response.json()['projects'][0]['description'] == new_project_1_description

def test_get_all_projects_by_existing_description(add_projects_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/projects', params={"description": new_project_2_description})
    assert response.status_code == 200
    assert len(response.json()['projects']) == 1
    assert response.json()['projects'][0]['title'] == new_project_2_title
    assert response.json()['projects'][0]['description'] == new_project_2_description

def test_get_all_projects_by_non_existing_id():
    response = requests.get(f'{DEFAULT_API_URL}/projects', params={"id": "999"})
    assert response.status_code == 200
    assert len(response.json()['projects']) == 0

# POST Tests
def test_post_new_project_all_parameters_filled_out():
    response = requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "New Project", "completed": False, "active": True, "description": "This is a new project"})
    assert response.status_code == 201
    assert response.json()["title"] == "New Project"
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "true"
    assert response.json()["description"] == "This is a new project"
    delete_project_by_id(int(response.json()["id"]))

def test_post_new_project_only_title_filled_out():
    response = requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "New Project"})
    assert response.status_code == 201
    assert response.json()["title"] == "New Project"
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == ""
    delete_project_by_id(int(response.json()["id"]))

@pytest.mark.actual_behaviour_passing
def test_post_new_project_no_title_filled_out():
    response = requests.post(f'{DEFAULT_API_URL}/projects', json={"description": "This is a new project"})
    assert response.status_code == 201
    assert response.json()["title"] == ""
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == "This is a new project"
    delete_project_by_id(int(response.json()["id"]))

def test_post_new_project_with_invalid_param():
    invalid_param = "invalid_param"
    response = requests.post(f'{DEFAULT_API_URL}/projects', json={"invalid_param": "bad_value"})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == f'Could not find field: {invalid_param}'

# HEAD Tests

def test_head_for_projects():
    response = requests.head(f'{DEFAULT_API_URL}/projects')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"