import pytest
import requests
from PartA.interoperability.utils import DEFAULT_API_URL, add_category_to_project, create_new_category, create_new_project, delete_category_by_id, delete_project_by_id

# Fixture to set up and tear down category and project
@pytest.fixture
def create_category_and_project():
    # Create a new category
    category_id = create_new_category("Test Category", "Category Description")
    
    # Create a new project
    project_id = create_new_project("Test Project", False, True, "Project Description")
    
    # Add the category to the project
    add_category_to_project(project_id, category_id)
    
    # Return the created category and project IDs
    yield category_id, project_id
    
    # Teardown: Delete both category and project after the test
    delete_category_by_id(category_id)
    delete_project_by_id(project_id)


### GET /projects/:id/categories - Get all categories related to a project
def test_get_categories_of_project(create_category_and_project):
    category_id, project_id = create_category_and_project
    
    # Retrieve categories related to the project
    response = requests.get(f"{DEFAULT_API_URL}/projects/{project_id}/categories")
    
    assert response.status_code == 200
    categories = response.json().get("categories", [])
    category_ids = [category["id"] for category in categories]
    
    # Check if the created category is linked to the project
    assert str(category_id) in category_ids

### POST /categories/:id/projects - Create a relationship between a project and a category that already exists
def test_post_category_to_project(create_category_and_project):
    category_id, project_id = create_category_and_project
    
    # Create a relationship between the project and category
    response = requests.post(f"{DEFAULT_API_URL}/categories/{category_id}/projects", json={"id": project_id})
    
    assert response.status_code == 201 or response.status_code == 200, f"Expected status 201 or 200 but got {response.status_code}"

### DELETE /projects/:id/categories/:id - Delete a relationship between a project and a category
def test_delete_category_from_project(create_category_and_project):
    category_id, project_id = create_category_and_project
    
    # Add the category to the project first
    response = requests.post(f"{DEFAULT_API_URL}/projects/{project_id}/categories", json={"id": category_id})
    assert response.status_code == 201
    
    # Now delete the relationship
    response = requests.delete(f"{DEFAULT_API_URL}/projects/{project_id}/categories/{category_id}")
    
    assert response.status_code == 200
    
    # Verify that the category has been removed from the project
    response = requests.get(f"{DEFAULT_API_URL}/projects/{project_id}/categories")
    categories = response.json().get("categories", [])
    category_ids = [category["id"] for category in categories]
    
    assert str(category_id) not in category_ids

### GET /categories/:id/projects - Expected behaviour failing due to known bug
@pytest.mark.expected_behaviour_failing
def test_get_projects_of_category(create_category_and_project):
    category_id, project_id = create_category_and_project
    
    # Retrieve projects related to the category
    response = requests.get(f"{DEFAULT_API_URL}/categories/{category_id}/projects")
    
    assert response.status_code == 200
    projects = response.json().get("projects", [])
    project_ids = [project["id"] for project in projects]
    
    # Check if the created project is linked to the category
    assert str(project_id) in project_ids

### DELETE /categories/:id/projects/:id - Expected behaviour failing due to known bug
@pytest.mark.expected_behaviour_failing
def test_delete_project_from_category(create_category_and_project):
    category_id, project_id = create_category_and_project
    
    # Add the category to the project first
    response = requests.post(f"{DEFAULT_API_URL}/projects/{project_id}/categories", json={"id": category_id})
    assert response.status_code == 201
    
    # Now delete the relationship from the category side
    response = requests.delete(f"{DEFAULT_API_URL}/categories/{category_id}/projects/{project_id}")
    
    assert response.status_code == 200
    
    # Verify that the project has been removed from the category
    response = requests.get(f"{DEFAULT_API_URL}/categories/{category_id}/projects")
    projects = response.json().get("projects", [])
    project_ids = [project["id"] for project in projects]
    
    assert str(project_id) not in project_ids
