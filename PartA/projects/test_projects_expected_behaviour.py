import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.project_utils import *

@pytest.mark.expected_behaviour_failing
def test_post_new_project_no_title_filled_out():
    response = requests.post(f'{DEFAULT_API_URL}/projects', json={"description": "This is a new project without a titleeeeee"})
    delete_project_by_id(int(response.json()["id"]))
    assert response.status_code == 400
    assert response.json()["errorMessages"][0] == "Title is required."
