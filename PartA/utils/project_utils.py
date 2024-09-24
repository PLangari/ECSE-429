import requests
from utils.default_variables import DEFAULT_API_URL

# Data for default project entity within the system
default_project_id = "1"
default_project_title = "Office Work"
default_project_completed = "false"
default_project_active= "false"
default_project_description = ""

# Data for default task entity within the system
default_task_id = "1"
default_task_title = "scan paperwork"
default_task_doneStatus = "false"
default_task_description = ""

# Data for new project to create and retrieve
new_project_1_title = "Yard Renovation"
new_project_1_completed = False
new_project_1_active= True
new_project_1_description = "Tidy up and freshen up the yard"

new_project_2_title = "Garage Cleanup"
new_project_2_completed = True
new_project_2_active= False
new_project_2_description = "Tidy up and organize the garage"

# Data for tasks/todo to link to project
new_task_1_title = "Mow the lawn"
new_task_1_doneStatus = False
new_task_1_description = "Mow the lawn and trim the edges"

new_task_2_title = "Plant flowers"
new_task_2_doneStatus = False
new_task_2_description = "Plant flowers in the garden"

# Data for categories to link to a project
new_category_1_title = "Home"
new_category_1_description = "Home Category"

new_category_2_title = "Garden"
new_category_2_description = "Garden Category"


# Helper Functions

def create_new_project(title, completed, active, description):
    response = requests.post(DEFAULT_API_URL + "/projects", json={"title": title, "completed": completed, "active": active, "description": description})
    assert response.status_code == 201
    return int(response.json()["id"])

def delete_project_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/projects/{id}")
    assert response.status_code == 200

def add_task_to_project(project_id, title, doneStatus, description):
    response = requests.post(DEFAULT_API_URL + f"/projects/{project_id}/tasks", json={"title": title, "doneStatus": doneStatus, "description": description})
    assert response.status_code == 201
    return int(response.json()["id"])

def delete_task_by_id(task_id):
    response = requests.delete(DEFAULT_API_URL + f"/todos/{task_id}")
    assert response.status_code == 200

def add_category_to_project(project_id, title, description):
    response = requests.post(DEFAULT_API_URL + f"/projects/{project_id}/categories", json={"title": title, "description": description})
    assert response.status_code == 201
    return int(response.json()["id"])

def delete_category_by_id(category_id):
    response = requests.delete(DEFAULT_API_URL + f"/categories/{category_id}")
    assert response.status_code == 200