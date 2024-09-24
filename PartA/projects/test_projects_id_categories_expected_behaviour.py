import requests
import pytest
from utils.default_variables import DEFAULT_API_URL
from utils.project_utils import *

@pytest.mark.expected_behaviour_failing
def test_get_categories_of_project_with_non_existing_id():
    nonexisting_id = "999"
    response = requests.get(f"{DEFAULT_API_URL}/projects/{nonexisting_id}/categories")
    assert response.status_code == 404
    assert response.json()["errorMessages"][0] == f"Project with id {nonexisting_id} not found"
  