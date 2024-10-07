import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.category_utils import *

# Setup
@pytest.fixture
def add_categories_to_database_and_cleanup():
    new_category_1_id = create_category(category_1_title, category_1_description)
    yield
    delete_category_by_id(new_category_1_id)
    
# OPTIONS Tests

def test_options_for_categories():
    response = requests.options(f'{DEFAULT_API_URL}/categories')
    assert response.status_code == 200
    assert response.headers["Allow"] == "OPTIONS, GET, HEAD, POST"
    
# GET Tests

def test_get_all_categories(add_categories_to_database_and_cleanup):
    response = requests.get(f'{DEFAULT_API_URL}/categories')
    assert response.status_code == 200
    assert len(response.json()['categories']) == 3
    
def test_get_all_categories_by_existing_id():
    response = requests.get(f'{DEFAULT_API_URL}/categories', params={"id": default_category_1_id})
    assert response.status_code == 200
    assert len(response.json()['categories']) == 1
    assert response.json()['categories'][0]['title'] == default_category_1_title
    assert response.json()['categories'][0]['description'] == default_category_1_description
    
def test_get_all_categories_by_non_existing_id():
    response = requests.get(f'{DEFAULT_API_URL}/categories', params={"id": 999})
    assert response.status_code == 200
    assert len(response.json()['categories']) == 0
    
def test_get_all_categories_by_existing_title():
    response = requests.get(f'{DEFAULT_API_URL}/categories', params={"title": default_category_1_title})
    assert response.status_code == 200
    assert len(response.json()['categories']) == 1
    assert response.json()['categories'][0]['title'] == default_category_1_title
    assert response.json()['categories'][0]['description'] == default_category_1_description
    
def test_get_all_categories_by_non_existing_title():
    response = requests.get(f'{DEFAULT_API_URL}/categories', params={"title": "Nonexistent"})
    assert response.status_code == 200
    assert len(response.json()['categories']) == 0
    
def test_get_all_categories_by_existing_description():
    response = requests.get(f'{DEFAULT_API_URL}/categories', params={"description": default_category_1_description})
    assert response.status_code == 200
    assert len(response.json()['categories']) == 2
    assert response.json()['categories'][0]['description'] == default_category_1_description
    assert response.json()['categories'][1]['description'] == default_category_2_description
    
def test_get_all_categories_by_non_existing_description():
    response = requests.get(f'{DEFAULT_API_URL}/categories', params={"description": "Nonexistent"})
    assert response.status_code == 200
    assert len(response.json()['categories']) == 0
    
# POST Tests
def test_post_new_category_all_parameters_filled_out():
    response = requests.post(f'{DEFAULT_API_URL}/categories', json={"title": "New Category", "description": "This is a new category"})
    assert response.status_code == 201
    assert response.json()["title"] == "New Category"
    assert response.json()["description"] == "This is a new category"
    # new_category_id = response.json()["id"]
    # response = requests.get(f'{DEFAULT_API_URL}/categories/{new_category_id}')
    # assert response.status_code == 200
    # assert response.json()['categories'][0]['title'] == "New Category"
    delete_category_by_id(int(response.json()["id"]))
    
def test_post_new_category_only_title_filled_out():
    response = requests.post(f'{DEFAULT_API_URL}/categories', json={"title": "New Category"})
    assert response.status_code == 201
    assert response.json()["title"] == "New Category"
    assert response.json()["description"] == ""
    delete_category_by_id(int(response.json()["id"]))
    
def test_post_new_category_no_title_filled_out():
    response = requests.post(f'{DEFAULT_API_URL}/categories', json={"description": "Category with no title"})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] ==  "title : field is mandatory"
    
def test_post_new_category_empty_title_filled_out():
    response = requests.post(f'{DEFAULT_API_URL}/categories', json={"title": ""})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] ==  "Failed Validation: title : can not be empty"
    
def test_post_new_category_with_invalid_param():
    invalid_param = "invalid"
    response = requests.post(f'{DEFAULT_API_URL}/categories', json={f"{invalid_param}": "bad_value"})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == f'Could not find field: {invalid_param}'

@pytest.mark.actual_behaviour_passing
def test_post_new_category_with_duplicate_title():
    response = requests.post(f'{DEFAULT_API_URL}/categories', json={"title": default_category_1_title})
    assert response.status_code == 201
    assert response.json()["title"] == default_category_1_title
    assert response.json()["description"] == ""
    delete_category_by_id(int(response.json()["id"]))

# HEAD Tests

def test_head_for_categories():
    response = requests.head(f'{DEFAULT_API_URL}/categories')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"