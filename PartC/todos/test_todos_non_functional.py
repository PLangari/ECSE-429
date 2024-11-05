import psutil
import pytest
import requests
from utils.default_variables import DEFAULT_API_URL
from utils.shared_util_functions import get_metrics, create_excel_file, append_data_to_excel, close_workbook
from utils.populating_db import populate_todos, delete_all_todos

max_number_of_objects = 1000
objects_to_increment_by = 100

@pytest.mark.order(1)
def test_create_todo_excel_file_and_data_sheets():
    create_excel_file("todo_performance_data.xlsx")

@pytest.mark.order(2)
def test_post_non_functional_metrics():
    for i in range(0, max_number_of_objects, objects_to_increment_by):
        # Populate the database with todo objects
        populate_todos(objects_to_increment_by)

        # Measure the response time for POST requests
        response_time_1, cpu_usage_1, mem_usage_1 = get_metrics("http://localhost:4567/todos", "POST", {"title": f"Object_With_{i}_Others_In_DB"})
        response_time_2, cpu_usage_2, mem_usage_2 = get_metrics("http://localhost:4567/todos", "POST", {"title": f"Object_With_{i}_Others_In_DB"})
        response_time_3, cpu_usage_3, mem_usage_3 = get_metrics("http://localhost:4567/todos", "POST", {"title": f"Object_With_{i}_Others_In_DB"})
        response_time_4, cpu_usage_4, mem_usage_4 = get_metrics("http://localhost:4567/todos", "POST", {"title": f"Object_With_{i}_Others_In_DB"})

        append_data_to_excel("todo_performance_data.xlsx", "POST Performance Data", 
                             [i, response_time_1, response_time_2, response_time_3, response_time_4,
                            cpu_usage_1, cpu_usage_2, cpu_usage_3, cpu_usage_4,
                            mem_usage_1, mem_usage_2, mem_usage_3, mem_usage_4])

    delete_all_todos()

@pytest.mark.order(3)
def test_put_non_functional_metrics():
    # Create default todo object to modify
    default_todo_object = requests.post(f'{DEFAULT_API_URL}/todos', json={"title": "Default_Todo_Object", "description": "Default_Description", "doneStatus": False})
    default_todo_object_id = default_todo_object.json()['id']

    for i in range(0, max_number_of_objects, objects_to_increment_by):
        # Populate the database with todo objects
        populate_todos(objects_to_increment_by)

        # Measure the response time for POST requests
        response_time_1, cpu_usage_1, mem_usage_1 = get_metrics(f"http://localhost:4567/todos/{default_todo_object_id}", "PUT", {"title": f"New Title for Default Object"})
        response_time_2, cpu_usage_2, mem_usage_2 = get_metrics(f"http://localhost:4567/todos/{default_todo_object_id}", "PUT", {"title": f"New Title for Default Object Again"})
        response_time_3, cpu_usage_3, mem_usage_3 = get_metrics(f"http://localhost:4567/todos/{default_todo_object_id}", "PUT", {"title": f"New Title for Default Object Again Again"})
        response_time_4, cpu_usage_4, mem_usage_4 = get_metrics(f"http://localhost:4567/todos/{default_todo_object_id}", "PUT", {"title": f"New Title for Default Object Again Again Again"})

        append_data_to_excel("todo_performance_data.xlsx", "PUT Performance Data", 
                             [i, response_time_1, response_time_2, response_time_3, response_time_4,
                            cpu_usage_1, cpu_usage_2, cpu_usage_3, cpu_usage_4,
                            mem_usage_1, mem_usage_2, mem_usage_3, mem_usage_4])

    delete_all_todos()

@pytest.mark.order(4)
def test_delete_non_functional_metrics():
    # Create default todo object to modify
    default_todo_object = requests.post(f'{DEFAULT_API_URL}/todos', json={"title": "Default_Todo_Object", "description": "Default_Description", "doneStatus": False})
    default_todo_object_id = default_todo_object.json()['id']

    for i in range(0, max_number_of_objects, objects_to_increment_by):
        # Populate the database with todo objects
        populate_todos(objects_to_increment_by)

        # Measure the response time for POST requests
        response_time_1, cpu_usage_1, mem_usage_1 = get_metrics(f"http://localhost:4567/todos/{default_todo_object_id}", "DELETE", None)
        response_time_2, cpu_usage_2, mem_usage_2 = get_metrics(f"http://localhost:4567/todos/{default_todo_object_id}", "DELETE", None)
        response_time_3, cpu_usage_3, mem_usage_3 = get_metrics(f"http://localhost:4567/todos/{default_todo_object_id}", "DELETE", None)
        response_time_4, cpu_usage_4, mem_usage_4 = get_metrics(f"http://localhost:4567/todos/{default_todo_object_id}", "DELETE", None)

        append_data_to_excel("todo_performance_data.xlsx", "DELETE Performance Data", 
                             [i, response_time_1, response_time_2, response_time_3, response_time_4,
                            cpu_usage_1, cpu_usage_2, cpu_usage_3, cpu_usage_4,
                            mem_usage_1, mem_usage_2, mem_usage_3, mem_usage_4])

    delete_all_todos()

@pytest.mark.order(5)
def test_close_workbook():
    close_workbook("todo_performance_data.xlsx")



