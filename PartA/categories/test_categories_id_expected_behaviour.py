import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.category_utils import *

# Setup
@pytest.fixture
def add_categories_to_database_and_cleanup():
    new_category_1_id = create_category(category_1_title, category_1_description)
    yield new_category_1_id
    delete_category_by_id(new_category_1_id)

# Failing POST Tests
@pytest.mark.expected_behaviour_failing
def test_post_category_with_id_and_duplicate_title(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.post(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": default_category_1_title})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "A category with this title already exists."
    response = get_category_by_id(new_category_1_id)
    assert response.json()["categories"][0]["title"] == category_1_title
    
# Failing PUT Tests
@pytest.mark.expected_behaviour_failing
def test_put_category_with_id_and_no_fields_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={})
    assert response.status_code == 200
    assert response.json()["title"] == category_1_title
    assert response.json()["description"] == category_1_description

@pytest.mark.expected_behaviour_failing
def test_put_category_with_id_and_title_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": category_2_title})
    assert response.status_code == 200
    assert response.json()["title"] == category_2_title
    assert response.json()["description"] == category_1_description
    
@pytest.mark.expected_behaviour_failing
def test_put_category_with_id_and_description_filled_out(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"description": category_2_description})
    assert response.status_code == 200
    assert response.json()["title"] == category_1_title
    assert response.json()["description"] == category_2_description
    
@pytest.mark.expected_behaviour_failing
def test_put_category_with_id_and_duplicate_title(add_categories_to_database_and_cleanup):
    new_category_1_id = add_categories_to_database_and_cleanup
    response = requests.put(f'{DEFAULT_API_URL}/categories/{new_category_1_id}', json={"title": default_category_1_title})
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "A category with this title already exists."
    response = get_category_by_id(new_category_1_id)
    assert response.json()["categories"][0]["title"] == category_1_title
    
