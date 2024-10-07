import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.category_utils import *

@pytest.mark.expected_behaviour_failing
def test_post_new_category_with_duplicate_title():
    response = requests.post(f'{DEFAULT_API_URL}/categories', json={"title": default_category_1_title})
    delete_category_by_id(int(response.json()["id"]))
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "A category with this title already exists."