import pytest
import requests
from PartA.interoperability.utils import DEFAULT_API_URL, add_task_to_category, create_new_category, create_new_task, delete_category_by_id, delete_task_by_id

# Fixture to set up and tear down category and task
@pytest.fixture
def create_category_and_task():
    # Create a new category
    category_id = create_new_category("Test Category", "Category Description")
    
    # Create a new task
    task_id = create_new_task("Test Task", "Task Description")
    
    # Add the task to the category
    add_task_to_category(category_id, task_id)
    
    # Return the created category and task IDs
    yield category_id, task_id
    
    # Teardown: Delete both task and category after the test
    delete_category_by_id(category_id)
    delete_task_by_id(task_id)


### GET /categories/:id/todos - Get all tasks related to a category
def test_get_tasks_of_category(create_category_and_task):
    category_id, task_id = create_category_and_task
    
    # Add the task to the category
    response = requests.post(f"{DEFAULT_API_URL}/categories/{category_id}/todos", json={"id": task_id})
    assert response.status_code == 201
    
    # Retrieve tasks related to the category
    response = requests.get(f"{DEFAULT_API_URL}/categories/{category_id}/todos")
    
    assert response.status_code == 200
    tasks = response.json().get("todos", [])
    task_ids = [task["id"] for task in tasks]
    
    # Check if the created task is linked to the category
    assert str(task_id) in task_ids

### POST /todos/:id/categories - Create a relationship between a category and a task that already exists
def test_post_task_to_category(create_category_and_task):
    category_id, task_id = create_category_and_task
    
    # Create a relationship between the category and task
    response = requests.post(f"{DEFAULT_API_URL}/todos/{task_id}/categories", json={"id": category_id})
    
    assert (response.status_code != 201 or response.status_code != 200), f"Expected relationship already exists but got {response.status_code}"

### DELETE /categories/:id/todos/:id - Delete a relationship between a category and a task
def test_delete_task_from_category(create_category_and_task):
    category_id, task_id = create_category_and_task
    
    # Add the task to the category first
    response = requests.post(f"{DEFAULT_API_URL}/categories/{category_id}/todos", json={"id": task_id})
    assert response.status_code == 201
    
    # Now delete the relationship
    response = requests.delete(f"{DEFAULT_API_URL}/categories/{category_id}/todos/{task_id}")
    
    assert response.status_code == 200
    
    # Verify that the task has been removed from the category
    response = requests.get(f"{DEFAULT_API_URL}/categories/{category_id}/todos")
    tasks = response.json().get("todos", [])
    task_ids = [task["id"] for task in tasks]
    
    assert str(task_id) not in task_ids

### GET /todos/:id/categories - Expected behaviour failing due to known bug
@pytest.mark.expected_behaviour_failing
def test_get_categories_of_task(create_category_and_task):
    category_id, task_id = create_category_and_task
    
    # Add the task to the category first
    response = requests.post(f"{DEFAULT_API_URL}/categories/{category_id}/todos", json={"id": task_id})
    assert response.status_code == 201
    
    # Retrieve categories related to the task
    response = requests.get(f"{DEFAULT_API_URL}/todos/{task_id}/categories")
    
    assert response.status_code == 200
    categories = response.json().get("categories", [])
    category_ids = [category["id"] for category in categories]
    
    # Check if the created category is linked to the task
    assert str(category_id) in category_ids

### DELETE /todos/:id/categories/:id- Expected behaviour failing due to known bug
@pytest.mark.expected_behaviour_failing
def test_delete_category_from_task(create_category_and_task):
    category_id, task_id = create_category_and_task
    
    # Add the task to the category first
    response = requests.post(f"{DEFAULT_API_URL}/categories/{category_id}/todos", json={"id": task_id})
    assert response.status_code == 201
    
    # Now delete the relationship from the task side
    response = requests.delete(f"{DEFAULT_API_URL}/todos/{task_id}/categories/{category_id}")
    
    assert response.status_code == 200
    
    # Verify that the category has been removed from the task
    response = requests.get(f"{DEFAULT_API_URL}/todos/{task_id}/categories")
    categories = response.json().get("categories", [])
    category_ids = [category["id"] for category in categories]
    
    assert str(category_id) not in category_ids
