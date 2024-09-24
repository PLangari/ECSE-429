import requests
from utils.default_variables import DEFAULT_API_URL

# Data for default project entity within the system
default_project_id = "1"
default_project_title = "Office Work"
default_project_completed = "false"
default_project_active= "false"
default_project_description = ""

new_project_1_title = "Yard Renovation"
new_project_1_completed = False
new_project_1_active= True
new_project_1_description = "Tidy up and freshen up the yard"

new_project_2_title = "Garage Cleanup"
new_project_2_completed = True
new_project_2_active= False
new_project_2_description = "Tidy up and organize the garage"

# Helper Functions

def create_new_project(title, completed, active, description):
    response = requests.post(DEFAULT_API_URL + "/projects", json={"title": title, "completed": completed, "active": active, "description": description})
    assert response.status_code == 201
    return int(response.json()["id"])

def delete_project_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/projects/{id}")
    assert response.status_code == 200