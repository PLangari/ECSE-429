import requests
from utils.default_variables import DEFAULT_API_URL

# Data for default todo entities within the system
default_todo_id_1 = "1"
default_todo_title_1 = "scan paperwork"
default_todo_doneStatus_1 = "false"
default_todo_description_1 = ""

default_todo_id_2 = "2"
default_todo_title_2 = "file paperwork"
default_todo_doneStatus_2 = "false"
default_todo_description_2 = ""

# Data for new todo to create and retrieve
new_todo_title_1 = "Order new printer"
new_todo_doneStatus_1 = True
new_todo_doneStatus_return_1 = "true"
new_todo_description_1 = "Order a new printer for the office"

new_todo_title_2 = "Order new business cards"
new_todo_doneStatus_2 = False
new_todo_doneStatus_return_2 = "false"
new_todo_description_2 = "Order new business cards for the team"

# Default data for categoires
default_category_id_1 = "1"
default_category_name_1 = "Office"
default_category_description_1 = ""

default_category_id_2 = "2"
default_category_name_2 = "Home"
default_category_description_2 = ""

# Default data for projects
default_project_id_1 = "1"
default_project_title_1 = "Office Work"
default_project_description_1 = ""
default_project_completed_1 = "false"
default_project_active_1 = "false"

def create_new_todo(title, completed, description):
    response = requests.post(DEFAULT_API_URL + "/todos", json={"title": title, "doneStatus": completed, "description": description})
    assert response.status_code == 201
    return int(response.json()["id"])

def delete_todo_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/todos/{id}")
    assert response.status_code == 200

def add_todo_to_category(todo_id, category_id):
    response = requests.post(DEFAULT_API_URL + f"/todos/{todo_id}/categories", json={"id": category_id})
    assert response.status_code == 201

def remove_todo_from_category(todo_id, category_id):
    response = requests.delete(DEFAULT_API_URL + f"/todos/{todo_id}/categories/{category_id}")
    assert response.status_code == 200

def add_todo_to_project(todo_id, project_id):
    response = requests.post(DEFAULT_API_URL + f"/todos/{todo_id}/tasksof", json={"id": project_id})
    assert response.status_code == 201

def remove_todo_from_project(todo_id, project_id):
    response = requests.delete(DEFAULT_API_URL + f"/todos/{todo_id}/tasksof/{project_id}")
    assert response.status_code == 200