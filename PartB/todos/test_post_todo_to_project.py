from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/todos/post_todo_to_project.feature", "Add an existing todo to an existing project")
def test_post_todo_to_project():
    pass

# Alternate Flow
@scenario("../features/todos/post_todo_to_project.feature", "Create a new project for the todo")
def test_post_todo_to_project_with_only_title():
    pass

# Error Flow
@scenario("../features/todos/post_todo_to_project.feature", "Add a todo to a nonexisting project")
def test_post_todo_to_project_with_invalid_parameter():
    pass

@when(parsers.parse('the user requests to add an existing todo "{todoId}" to an existing project "{projectId}"'))
def post_todo_to_project(todoId, projectId, returnedResponse):
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    pId = sortedProjects[int(projectId)]['id']
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos')
    sortedTodos = sorted(allTodos.json()['todos'], key=lambda todo: todo['id'])
    tId = sortedTodos[int(todoId)]['id']

    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/todos/{tId}/tasksof', json={"id": pId})
    print(returnedResponse)

@when(parsers.parse('the user requests to add an existing todo "{todoId}" to a new project "{projectName}"'))
def post_todo_to_project_with_only_title(todoId, projectName, returnedResponse):
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos')
    sortedTodos = sorted(allTodos.json()['todos'], key=lambda todo: todo['id'])
    tId = sortedTodos[int(todoId)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/todos/{tId}/tasksof', json={"title": projectName})

@when(parsers.parse('the user requests to add an existing todo "{todoId}" to a nonexisting project "{projectId}"'))
def post_todo_to_project_with_invalid_parameter(todoId, projectId, returnedResponse):
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos')
    sortedTodos = sorted(allTodos.json()['todos'], key=lambda todo: todo['id'])
    tId = sortedTodos[int(todoId)]['id']
    returnedResponse['response'] = requests.post(f'{DEFAULT_API_URL}/todos/{tId}/tasksof', json={"id": projectId})
    
@then(parsers.parse('the new project object "{projectName}" shall be returned'))
def verify_new_project_with_only_title(projectName, returnedResponse):
    returnData = returnedResponse["response"].json()
    assert returnData["title"] == projectName
    delete_project_by_id(returnData['id'])