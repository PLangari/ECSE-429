import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.category_utils import *

#Setup
@pytest.fixture
def add_categories_to_database_and_cleanup():
    new_category_1_id = create_category(category_1_title, category_1_description)
    yield new_category_1_id
    delete_category_by_id(new_category_1_id)

# HEAD Tests
def test_head_categories_with_existing_id():
    response = requests.head(f'{DEFAULT_API_URL}/categories/{default_category_1_id}')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

def test_head_categories_with_non_existing_id():
    nonexistent_id = 999
    response = requests.head(f'{DEFAULT_API_URL}/categories/{nonexistent_id}')
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"

# OPTIONS Tests
def test_options_for_category_with_id():
    response = requests.options(f'{DEFAULT_API_URL}/categories/{default_category_1_id}')
    assert response.status_code == 200
    assert response.headers["Allow"] == "OPTIONS, GET, HEAD, POST, PUT, DELETE"
    
# GET Tests
def test_get_category_by_existing_id():
    response = requests.get(f'{DEFAULT_API_URL}/categories/{default_category_1_id}')
    assert response.status_code == 200
    assert len(response.json()["categories"]) == 1
    assert response.json()["categories"][0]["title"] == default_category_1_title

def test_get_category_by_non_existing_id():
    nonexistent_id = 999
    response = requests.get(f'{DEFAULT_API_URL}/categories/{nonexistent_id}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find an instance with categories/{nonexistent_id}"

# POST Tests
def test_post_category_with_id_and_all_fields_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.post(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": category_2_title, "description": category_2_description})
    assert response.status_code == 200
    assert response.json()["title"] == category_2_title
    assert response.json()["description"] == category_2_description
    
def test_post_category_with_id_and_no_fields_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.post(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={})
    assert response.status_code == 200
    assert response.json()["title"] == category_1_title
    assert response.json()["description"] == category_1_description

def test_post_category_with_id_and_title_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.post(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": category_2_title})
    assert response.status_code == 200
    assert response.json()["title"] == category_2_title
    assert response.json()["description"] == category_1_description
    
def test_post_category_with_id_and_description_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.post(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"description": category_2_description})
    assert response.status_code == 200
    assert response.json()["title"] == category_1_title
    assert response.json()["description"] == category_2_description
    
def test_post_category_with_id_and_empty_title_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.post(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": ""})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "Failed Validation: title : can not be empty"
    response = get_category_by_id(new_category_1_id)
    assert response.json()["categories"][0]["title"] == category_1_title
    assert response.json()["categories"][0]["description"] == category_1_description

def test_post_category_with_non_existing_id():
    nonexistent_id = 999
    response = requests.post(f'{DEFAULT_API_URL}/categories/{nonexistent_id}', json={"title": category_1_title, "description": category_1_description})
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"No such category entity instance with GUID or ID {nonexistent_id} found"
    
def test_post_category_with_id_and_invalid_field(add_categories_to_database_and_cleanup):
    invalid_field = "invalid_field"
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.post(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": category_1_title, "description": category_1_description, f"{invalid_field}": "Invalid"})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == f"Could not find field: {invalid_field}"
    
@pytest.mark.actual_behaviour_passing
def test_post_category_with_id_and_duplicate_title(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.post(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": default_category_1_title})
    assert response.status_code == 200
    assert response.json()["title"] == default_category_1_title
    assert response.json()["description"] == category_1_description
    
# PUT Tests
def test_put_category_with_id_and_all_fields_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": category_2_title, "description": category_2_description})
    assert response.status_code == 200
    assert response.json()["title"] == category_2_title
    assert response.json()["description"] == category_2_description
    
@pytest.mark.actual_behaviour_passing
def test_put_category_with_id_and_no_fields_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "title : field is mandatory"
    response = get_category_by_id(new_category_1_id)
    assert response.json()["categories"][0]["title"] == category_1_title
    assert response.json()["categories"][0]["description"] == category_1_description

@pytest.mark.actual_behaviour_passing
def test_put_category_with_id_and_title_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": category_2_title})
    assert response.status_code == 200
    assert response.json()["title"] == category_2_title
    assert response.json()["description"] == ""
    
@pytest.mark.actual_behaviour_passing
def test_put_category_with_id_and_description_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"description": category_2_description})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "title : field is mandatory"
    response = get_category_by_id(new_category_1_id)
    assert response.json()["categories"][0]["title"] == category_1_title
    assert response.json()["categories"][0]["description"] == category_1_description
    
def test_put_category_with_id_and_empty_title_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": ""})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "Failed Validation: title : can not be empty"
    response = get_category_by_id(new_category_1_id)
    assert response.json()["categories"][0]["title"] == category_1_title

def test_put_category_with_non_existing_id():
    nonexistent_id = 999
    response = requests.put(f'{DEFAULT_API_URL}/categories/{nonexistent_id}', json={"title": category_1_title, "description": category_1_description})
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Invalid GUID for {nonexistent_id} entity category"
    
def test_put_category_with_id_and_invalid_field(add_categories_to_database_and_cleanup):
    invalid_field = "invalid_field"
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": category_1_title, "description": category_1_description, f"{invalid_field}": "Invalid"})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == f"Could not find field: {invalid_field}"
    
@pytest.mark.actual_behaviour_passing
def test_put_category_with_id_and_duplicate_title(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": default_category_1_title})
    assert response.status_code == 200
    assert response.json()["title"] == default_category_1_title
    
# DELETE Tests
def test_delete_category_with_existing_id():
    new_category_1_id = create_category(category_1_title, "")
    response = requests.delete(f'{DEFAULT_API_URL}/categories/{new_category_1_id}')
    assert response.status_code == 200
    response = requests.get(f'{DEFAULT_API_URL}/categories/{new_category_1_id}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find an instance with categories/{new_category_1_id}"

def test_delete_category_with_nonexistent_id():
    nonexistent_id = 999
    response = requests.delete(f'{DEFAULT_API_URL}/categories/{nonexistent_id}')
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Could not find any instances with categories/{nonexistent_id}"