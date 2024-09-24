import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.project_utils import *

# Setup/Teardown Methods
@pytest.fixture
def create_project_with_categories():
    id_of_new_project = create_new_project(new_project_1_title, new_project_1_completed, new_project_1_active, new_project_1_description)
    id_of_new_category_1 = add_category_to_project(id_of_new_project, new_category_1_title, new_category_1_description)
    id_of_new_category_2 = add_category_to_project(id_of_new_project, new_category_2_title, new_category_2_description)
    yield id_of_new_project, id_of_new_category_1, id_of_new_category_2
    delete_project_by_id(id_of_new_project)
    delete_category_by_id(id_of_new_category_1)
    delete_category_by_id(id_of_new_category_2)

# DELETE Tests
def test_delete_category_by_id_with_existing_id(create_project_with_categories):
    id_of_new_project, id_of_new_category_1, id_of_new_category_2 = create_project_with_categories
    # See categories were added
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories")
    responseOrderedById=sorted(response.json()["categories"], key=lambda x: x["id"])
    assert response.status_code == 200
    assert len(responseOrderedById) == 2
    assert responseOrderedById[0]["id"] == str(id_of_new_category_1)
    assert responseOrderedById[0]["title"] == new_category_1_title
    assert responseOrderedById[0]["description"] == new_category_1_description
    assert responseOrderedById[1]["id"] == str(id_of_new_category_2)
    assert responseOrderedById[1]["title"] == new_category_2_title
    assert responseOrderedById[1]["description"] == new_category_2_description
    
    # Delete first category
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories/{id_of_new_category_1}")
    assert response.status_code == 200
    # Check if category was deleted
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories")
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["id"] == str(id_of_new_category_2)
    assert response.json()["categories"][0]["title"] == new_category_2_title
    assert response.json()["categories"][0]["description"] == new_category_2_description
    
    # Delete second category
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories/{id_of_new_category_2}")
    assert response.status_code == 200
    # Check if category was deleted
    response = requests.get(f"{DEFAULT_API_URL}/projects/{id_of_new_project}/categories")
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 0

def test_delete_category_by_id_with_nonexistent_id():
    nonexisting_id = "999"
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{default_project_id}/categories/{nonexisting_id}")
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find any instances with projects/{default_project_id}/categories/{nonexisting_id}"
