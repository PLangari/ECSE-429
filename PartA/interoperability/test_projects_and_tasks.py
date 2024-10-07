import pytest
import requests
from PartA.interoperability.utils import DEFAULT_API_URL, create_new_project, create_new_task, delete_project_by_id, delete_task_by_id

@pytest.fixture
def create_task_and_project():
    # Create a new project
    project_id = create_new_project("Test Project", False, True, "Project Description")
    
    # Create a new task
    task_id = create_new_task("Test Task", "Task Description")
    
    # Add the task to the project
    response = requests.post(f"{DEFAULT_API_URL}/projects/{project_id}/tasks", json={"id": task_id})
    assert response.status_code == 201
    
    yield project_id, task_id
    
    delete_task_by_id(task_id)
    delete_project_by_id(project_id)

### GET /tasks/:id/projects
def test_get_projects_of_task(create_task_and_project):
    project_id, task_id = create_task_and_project
    
    response = requests.get(f"{DEFAULT_API_URL}/todos/{task_id}/tasksof")
    
    assert response.status_code == 200
    projects = response.json().get("projects", [])
    project_ids = [project["id"] for project in projects]
    
    assert str(project_id) in project_ids

### GET /projects/:id/tasks - Expected behaviour failing due to known bug
@pytest.mark.expected_behaviour_failing
def test_get_tasks_of_project(create_task_and_project):
    project_id, task_id = create_task_and_project
    
    response = requests.get(f"{DEFAULT_API_URL}/projects/{project_id}/tasks")
    
    assert response.status_code == 200
    tasks = response.json().get("tasks", [])
    task_ids = [task["id"] for task in tasks]
    
    assert str(task_id) in task_ids


### POST /tasks/:id/projects - Expected behaviour failing due to known bug
@pytest.mark.expected_behaviour_failing
def test_post_task_to_project(create_task_and_project):
    project_id, task_id = create_task_and_project
    
    response = requests.post(f"{DEFAULT_API_URL}/todos/{task_id}/tasksof", json={"id": project_id})

    assert response.status_code == 201 or response.status_code == 200, f"Expected 201/200 but got {response.status_code}"

    response = requests.get(f"{DEFAULT_API_URL}/projects/{project_id}/tasks")

    assert response.status_code == 200

    tasks = response.json().get("tasks", [])
    task_ids = [task["id"] for task in tasks]

    assert str(task_id) in task_ids


### DELETE /projects/:id/tasks/:id
def test_delete_task_from_project(create_task_and_project):
    project_id, task_id = create_task_and_project
    
    response = requests.post(f"{DEFAULT_API_URL}/projects/{project_id}/tasks", json={"id": task_id})
    assert response.status_code == 201
    
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{project_id}/tasks/{task_id}")
    
    assert response.status_code == 200
    
    response = requests.get(f"{DEFAULT_API_URL}/projects/{project_id}/tasks")
    tasks = response.json().get("todos", [])
    task_ids = [task["id"] for task in tasks]
    
    assert str(task_id) not in task_ids


### DELETE /tasks/:id/projects/:id
def test_delete_project_from_task(create_task_and_project):
    project_id, task_id = create_task_and_project
    
    response = requests.post(f"{DEFAULT_API_URL}/projects/{project_id}/tasks", json={"id": task_id})
    assert response.status_code == 201
    
    response = requests.get(f"{DEFAULT_API_URL}/todos/{task_id}/tasksof")
    projects = response.json().get("projects", [])
    project_ids = [project["id"] for project in projects]

    assert str(project_id) in project_ids

    response = requests.delete(f"{DEFAULT_API_URL}/todos/{task_id}/tasksof/{project_id}")
    
    assert response.status_code == 200
    
    response = requests.get(f"{DEFAULT_API_URL}/todos/{task_id}/tasksof")
    projects = response.json().get("projects", [])
    project_ids = [project["id"] for project in projects]
    
    assert str(project_id) not in project_ids
