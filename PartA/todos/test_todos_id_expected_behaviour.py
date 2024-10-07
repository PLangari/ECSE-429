import requests
import pytest
from utils.default_variables import DEFAULT_API_URL
from utils.todos_utils import *

@pytest.mark.expected_behaviour_failing
def test_put_todo_with_id_and_only_description_filled_out():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.put(f'{DEFAULT_API_URL}/todos/{id_of_new_todo_1}', json={"description": new_todo_description_2})
    assert response.status_code == 200
    assert response.json()["title"] == new_todo_title_1
    assert response.json()["doneStatus"] == new_todo_doneStatus_return_1
    assert response.json()["description"] == new_todo_description_2
    delete_todo_by_id(id_of_new_todo_1)

@pytest.mark.expected_behaviour_failing
def test_put_todo_with_id_and_only_doneStatus_filled_out():
    id_of_new_todo = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    response = requests.put(f'{DEFAULT_API_URL}/todos/{id_of_new_todo}', json={"doneStatus": new_todo_doneStatus_2})
    assert response.status_code == 200
    assert response.json()["title"] == new_todo_title_1
    assert response.json()["doneStatus"] == new_todo_doneStatus_return_2
    assert response.json()["description"] == new_todo_description_1
    delete_todo_by_id(id_of_new_todo)
