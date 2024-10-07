import requests
from utils.default_variables import DEFAULT_API_URL

# Data for default categories within the system
default_category_1_id = "1"
default_category_1_title = "Office"
default_category_1_description = ""

default_category_2_id = "2"
default_category_2_title = "Home"
default_category_2_description = ""

# Data for new categories to create and retrieve
category_1_title = "School"
category_1_description = "School category"

category_2_title = "Garden"
category_2_description = "Garden category"

# Helper Functions
def create_category(title, description): 
    response = requests.post(DEFAULT_API_URL + "/categories", json={"title": title, "description": description})
    assert response.status_code == 201
    return int(response.json()["id"])

def delete_category_by_id(id):
    response = requests.delete(DEFAULT_API_URL + f"/categories/{id}")
    assert response.status_code == 200
    
def get_category_by_id(id):
    response = requests.get(DEFAULT_API_URL + f"/categories/{id}")
    assert response.status_code == 200
    return response