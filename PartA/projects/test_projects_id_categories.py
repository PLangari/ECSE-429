import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.project_utils import *

# Setup/Teardown Methods
@pytest.fixture
def create_project_without_categories():
    id_of_new_project = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    yield id_of_new_project
    delete_project_by_id(id_of_new_project)

@pytest.fixture
def create_project_with_categories():
    id_of_new_project = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    id_of_new_category_1 = add_category_to_project(id_of_new_project, new_category_1_title, new_category_1_description)
    id_of_new_category_2 = add_category_to_project(id_of_new_project, new_category_2_title, new_category_2_description)
    yield id_of_new_project, id_of_new_category_1, id_of_new_category_2
    delete_project_by_id(id_of_new_project)
    delete_category_by_id(id_of_new_category_1)
    delete_category_by_id(id_of_new_category_2)

# GET Tests
def test_get_categories_of_project_with_existing_id_and_existing_categories(create_project_with_categories):
    id_of_new_project, id_of_new_category_1, id_of_new_category_2 = create_project_with_categories
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories")
    responseOrderedById=sorted(response.json()["categories"], key=lambda x: x["id"])
    assert response.status_code == 200
    assert len(responseOrderedById) == 2
    assert responseOrderedById[0]["id"] == str(id_of_new_category_1)
    assert responseOrderedById[0]["description"] == new_category_1_description
    assert responseOrderedById[1]["id"] == str(id_of_new_category_2)
    assert responseOrderedById[1]["description"] == new_category_2_description

def test_get_categories_of_project_with_existing_id_and_no_categories(create_project_without_categories):
    id_of_new_project = create_project_without_categories
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories")
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 0

@pytest.mark.actual_behaviour_working
def test_get_categories_of_project_with_non_existing_id(create_project_with_categories):
    nonexisting_id = "999"
    response = requests.get(f"{DEFAULT_API_URL}/projects/{nonexisting_id}/categories")
    assert response.status_code == 200
    assert len(response.json()["categories"]) != 0

def test_get_categories_of_project_with_existing_id_by_valid_title(create_project_with_categories):
    id_of_new_project = create_project_with_categories
    # Retrieve first category
    response = requests.get(f'{DEFAULT_API_URL}/projects/{id_of_new_project}/categories', params={"title": new_category_1_title})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["title"] == new_category_1_title
    assert response.json()["categories"][0]["description"] == new_category_1_description
    # Retrieve second category
    response = requests.get(f'{DEFAULT_API_URL}/projects/{id_of_new_project}/categories', params={"title": new_category_2_title})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["title"] == new_category_2_title
    assert response.json()["categories"][0]["description"] == new_category_2_description

def test_get_categories_of_project_with_existing_id_by_valid_description(create_project_with_categories):
    id_of_new_project = create_project_with_categories
    # Retrieve first category
    response = requests.get(f'{DEFAULT_API_URL}/projects/{id_of_new_project}/categories', params={"description": new_category_1_description})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["title"] == new_category_1_title
    assert response.json()["categories"][0]["description"] == new_category_1_description
    # Retrieve second category
    response = requests.get(f'{DEFAULT_API_URL}/projects/{id_of_new_project}/categories', params={"description": new_category_2_description})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["title"] == new_category_2_title
    assert response.json()["categories"][0]["description"] == new_category_2_description
    
def test_get_categories_of_project_with_existing_id_by_nonexistent_title():
    response = requests.get(f'{DEFAULT_API_URL}/projects/{default_project_id}/categories', params={"title": "Nonexistent"})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 0

def test_get_categories_of_project_with_existing_id_by_nonexistent_description():
    response = requests.get(f'{DEFAULT_API_URL}/projects/{default_project_id}/categories', params={"description": "Nonexistent"})
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 0

# HEAD Tests
def test_head_projects_id_categories():
    response = requests.head(f"{DEFAULT_API_URL}/projects/1/categories")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

# POST Tests
def test_post_new_category_to_project_with_existing_id_and_all_fields_filled_out(create_project_without_categories):
    id_of_new_project = create_project_without_categories
    response = requests.post(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories", json={"title": new_category_1_title, "description": new_category_1_description})
    assert response.status_code == 201
    assert response.json()["title"] == new_category_1_title
    assert response.json()["description"] == new_category_1_description
    # Ensure category was added
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories")
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["title"] == new_category_1_title
    assert response.json()["categories"][0]["description"] == new_category_1_description
    delete_category_by_id(int(response.json()["categories"][0]["id"]))

def test_post_new_category_to_project_with_non_existing_id():
    nonexisting_id = "999"
    response = requests.post(f"{DEFAULT_API_URL}/projects/{nonexisting_id}/categories", json={"title": new_category_1_title, "description": new_category_1_description})
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find parent thing for relationship projects/{nonexisting_id}/categories"

def test_post_new_category_to_project_with_existing_id_and_invalid_field(create_project_without_categories):
    invalid_field = "invalid"
    id_of_new_project = create_project_without_categories
    response = requests.post(f'{DEFAULT_API_URL}/projects/{id_of_new_project}/categories', json={f"{invalid_field}": "Doesn't matter"})
    assert response.status_code == 400

def test_post_new_category_to_project_with_existing_id_and_no_title_filled_out(create_project_without_categories):
    id_of_new_project = create_project_without_categories
    response = requests.post(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories", json={"description": new_category_1_description})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "title : field is mandatory"

def test_post_new_category_to_project_with_existing_id_and_only_title_filled_out(create_project_without_categories):
    id_of_new_project = create_project_without_categories
    response = requests.post(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories", json={"title": new_category_1_title})
    assert response.status_code == 201
    assert response.json()["title"] == new_category_1_title
    assert response.json()["description"] == ""
    # Ensure category was added
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories")
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["title"] == new_category_1_title
    assert response.json()["categories"][0]["description"] == ""
    delete_category_by_id(int(response.json()["categories"][0]["id"]))

