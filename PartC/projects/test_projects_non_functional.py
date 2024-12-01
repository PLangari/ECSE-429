import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.shared_util_functions import get_metrics, create_excel_file, append_data_to_excel, close_workbook
from utils.populating_db import populate_projects, delete_all_projects
import os
print(os.getcwd())

max_number_of_objects = 10000
objects_to_increment_by = 25

@pytest.mark.order(1)
def test_create_project_excel_file_and_data_sheets():
    create_excel_file("project_performance_data.xlsx")

@pytest.mark.order(2)
def test_post_non_functional_metrics():
    for i in range(0, max_number_of_objects, objects_to_increment_by):
        # Populate the database with project objects
        populate_projects(objects_to_increment_by)

        # Measure the response time for POST requests
        response_time_1, cpu_usage_1, mem_usage_1 = get_metrics("http://localhost:4567/projects", "POST", {"title": f"Object_With_{i}_Others_In_DB"})
        response_time_2, cpu_usage_2, mem_usage_2 = get_metrics("http://localhost:4567/projects", "POST", {"title": f"Object_With_{i}_Others_In_DB"})
        response_time_3, cpu_usage_3, mem_usage_3 = get_metrics("http://localhost:4567/projects", "POST", {"title": f"Object_With_{i}_Others_In_DB"})
        response_time_4, cpu_usage_4, mem_usage_4 = get_metrics("http://localhost:4567/projects", "POST", {"title": f"Object_With_{i}_Others_In_DB"})

        append_data_to_excel("project_performance_data.xlsx", "POST Performance Data", 
                             [i, response_time_1, response_time_2, response_time_3, response_time_4,
                            cpu_usage_1, cpu_usage_2, cpu_usage_3, cpu_usage_4,
                            mem_usage_1, mem_usage_2, mem_usage_3, mem_usage_4])

    delete_all_projects()

@pytest.mark.order(3)
def test_put_non_functional_metrics():
    # Create default project object to modify
    default_project_object = requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "Default_project_Object", "description": "Default_Description"})
    default_project_object_id = default_project_object.json()['id']

    for i in range(0, max_number_of_objects, objects_to_increment_by):
        # Populate the database with project objects
        populate_projects(objects_to_increment_by)

        # Measure the response time for PUT requests
        response_time_1, cpu_usage_1, mem_usage_1 = get_metrics(f"http://localhost:4567/projects/{default_project_object_id}", "PUT", {"title": f"New Title for Default Object"})
        response_time_2, cpu_usage_2, mem_usage_2 = get_metrics(f"http://localhost:4567/projects/{default_project_object_id}", "PUT", {"title": f"New Title for Default Object Again"})
        response_time_3, cpu_usage_3, mem_usage_3 = get_metrics(f"http://localhost:4567/projects/{default_project_object_id}", "PUT", {"title": f"New Title for Default Object Again Again"})
        response_time_4, cpu_usage_4, mem_usage_4 = get_metrics(f"http://localhost:4567/projects/{default_project_object_id}", "PUT", {"title": f"New Title for Default Object Again Again Again"})

        append_data_to_excel("project_performance_data.xlsx", "PUT Performance Data", 
                             [i, response_time_1, response_time_2, response_time_3, response_time_4,
                            cpu_usage_1, cpu_usage_2, cpu_usage_3, cpu_usage_4,
                            mem_usage_1, mem_usage_2, mem_usage_3, mem_usage_4])

    delete_all_projects()

@pytest.mark.order(4)
def test_delete_non_functional_metrics():
    # Create default project object to modify
    default_project_object = requests.post(f'{DEFAULT_API_URL}/projects', json={"title": "Default_project_Object", "description": "Default_Description"})
    default_project_object_id = default_project_object.json()['id']

    for i in range(0, max_number_of_objects, objects_to_increment_by):
        # Populate the database with project objects
        populate_projects(objects_to_increment_by)

        # Measure the response time for DELETE requests
        response_time_1, cpu_usage_1, mem_usage_1 = get_metrics(f"http://localhost:4567/projects/{default_project_object_id}", "DELETE", None)
        response_time_2, cpu_usage_2, mem_usage_2 = get_metrics(f"http://localhost:4567/projects/{default_project_object_id}", "DELETE", None)
        response_time_3, cpu_usage_3, mem_usage_3 = get_metrics(f"http://localhost:4567/projects/{default_project_object_id}", "DELETE", None)
        response_time_4, cpu_usage_4, mem_usage_4 = get_metrics(f"http://localhost:4567/projects/{default_project_object_id}", "DELETE", None)

        append_data_to_excel("project_performance_data.xlsx", "DELETE Performance Data", 
                             [i, response_time_1, response_time_2, response_time_3, response_time_4,
                            cpu_usage_1, cpu_usage_2, cpu_usage_3, cpu_usage_4,
                            mem_usage_1, mem_usage_2, mem_usage_3, mem_usage_4])

    delete_all_projects()

@pytest.mark.order(5)
def test_close_workbook():
    close_workbook("project_performance_data.xlsx")


