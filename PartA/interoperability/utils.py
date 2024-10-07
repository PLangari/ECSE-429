import requests
from PartA.utils.default_variables import DEFAULT_API_URL

# Helper Functions
def create_new_category(title, description):
    """
    Creates a new category with the given title and description.
    Returns the ID of the newly created category.
    """
    response = requests.post(DEFAULT_API_URL + "/categories", json={"title": title, "description": description})
    assert response.status_code == 201
    return response.json()["id"]

def delete_category_by_id(category_id):
    """
    Deletes a category by its ID.
    """
    response = requests.delete(DEFAULT_API_URL + f"/categories/{category_id}")
    assert response.status_code == 200

def add_task_to_category(category_id, task_id):
    """
    Creates a relationship between a category and a task by task ID.
    """
    response = requests.post(f"{DEFAULT_API_URL}/categories/{category_id}/todos", json={"id": task_id})
    
    # Check if the relationship creation was successful
    if response.status_code != 201:
        print(f"Error: {response.status_code}, {response.text}")
    
    assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"

def remove_task_from_category(category_id, task_id):
    """
    Removes a task from a category by deleting the relationship between them.
    """
    response = requests.delete(f"{DEFAULT_API_URL}/categories/{category_id}/todos/{task_id}")
    assert response.status_code == 200

def get_tasks_of_category(category_id):
    """
    Retrieves all tasks related to the given category ID.
    """
    response = requests.get(f"{DEFAULT_API_URL}/categories/{category_id}/todos")
    assert response.status_code == 200
    return response.json()["todos"]

def get_categories_of_task(task_id):
    """
    Retrieves all categories related to the given task ID.
    """
    response = requests.get(f"{DEFAULT_API_URL}/todos/{task_id}/categories")
    assert response.status_code == 200
    return response.json()["categories"]

def remove_category_from_task(task_id, category_id):
    """
    Removes a category from a task by deleting the relationship between them.
    """
    response = requests.delete(f"{DEFAULT_API_URL}/todos/{task_id}/categories/{category_id}")
    assert response.status_code == 200

def create_new_project(title, completed, active, description):
    """
    Creates a new project with the given title, completed status, active status, and description.
    Returns the ID of the newly created project.
    """
    response = requests.post(DEFAULT_API_URL + "/projects", json={
        "title": title,
        "completed": completed,
        "active": active,
        "description": description
    })
    assert response.status_code == 201
    return response.json()["id"]

def delete_project_by_id(project_id):
    """
    Deletes a project by its ID.
    """
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{project_id}")
    assert response.status_code == 200

def add_category_to_project(project_id, category_id):
    """
    Adds a category to a project by creating a relationship between them.
    """
    response = requests.post(f"{DEFAULT_API_URL}/projects/{project_id}/categories", json={"id": category_id})
    assert response.status_code == 201

def remove_category_from_project(project_id, category_id):
    """
    Removes a category from a project by deleting the relationship.
    """
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{project_id}/categories/{category_id}")
    assert response.status_code == 200

def create_new_task(title, description, doneStatus=False):
    """
    Creates a new task/todo with the given title, description, and done status.
    Returns the ID of the newly created task.
    """
    response = requests.post(DEFAULT_API_URL + "/todos", json={
        "title": title,
        "doneStatus": doneStatus,
        "description": description
    })
    assert response.status_code == 201
    return response.json()["id"]

def delete_task_by_id(task_id):
    """
    Deletes a task/todo by its ID.
    """
    response = requests.delete(DEFAULT_API_URL + f"/todos/{task_id}")
    assert response.status_code == 200
