import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.project_utils import *

@pytest.mark.expected_behaviour_failing
def test_put_project_with_id_and_only_title_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"title": new_project_2_title})
    delete_project_by_id(id_of_new_project_1)
    assert response.status_code == 200
    assert response.json()["title"] == new_project_2_title
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "true"
    assert response.json()["description"] == new_project_1_description

@pytest.mark.expected_behaviour_failing
def test_put_project_with_id_and_only_description_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"description": new_project_2_description})
    delete_project_by_id(id_of_new_project_1)
    assert response.status_code == 200
    assert response.json()["title"] == new_project_1_title
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "true"
    assert response.json()["description"] == new_project_2_description

@pytest.mark.expected_behaviour_failing
def test_put_with_id_and_only_completed_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"completed": True})
    delete_project_by_id(id_of_new_project_1)
    assert response.status_code == 200
    assert response.json()["title"] == new_project_1_title
    assert response.json()["completed"] == "true"
    assert response.json()["active"] == "true"
    assert response.json()["description"] == new_project_1_description

@pytest.mark.expected_behaviour_failing
def test_put_with_id_and_only_active_filled_out():
    id_of_new_project_1 = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    response = requests.put(f'{DEFAULT_API_URL}/projects/{id_of_new_project_1}', json={"active": False})
    delete_project_by_id(id_of_new_project_1)
    assert response.status_code == 200
    assert response.json()["title"] == new_project_1_title
    assert response.json()["completed"] == "false"
    assert response.json()["active"] == "false"
    assert response.json()["description"] == new_project_1_description
