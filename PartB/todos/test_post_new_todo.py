from pytest_bdd import scenario, given, when, then, parsers
from utils.default_variables import DEFAULT_API_URL
from utils.general_step_definitions import *
import requests

# Normal Flow
@scenario("../features/todos/post_new_todo.feature", "Post a new todo with all parameter fields filled out")
def test_post_new_todo():
    pass

# Alternate Flow
@scenario("../features/todos/post_new_todo.feature", "Post a new todo with only the title field filled out")
def test_post_new_todo_with_only_title():
    pass

# Error Flow
@scenario("../features/todos/post_new_todo.feature", "Post a new todo without a title")
def test_post_new_todo_with_invalid_parameter():
    pass

@when(parsers.parse('the user requests to post a new todo with title "{title}", description "{description}", doneStatus "{doneStatus}" as part of projectId "{projectId}" and categoryId "{categoryId}"'))
def post_new_todo_with_all_parameters(title, description, doneStatus, projectId, categoryId, returnedResponse):
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    pId = sortedProjects[int(projectId)]['id']
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    cId = sortedCategories[int(categoryId)]['id']
    if doneStatus == "true":
        doneStatus = True
    else:
        doneStatus = False
    returnedResponse["response"] = requests.post(DEFAULT_API_URL + "/todos", json={"title": title, "doneStatus": doneStatus, "description": description, "tasksof": [{"id": pId}], "categories": [{"id":cId}]})

@when(parsers.parse('the user requests to post a new todo with title "{title}" only'))
def post_new_todo_with_only_title(title, returnedResponse):
    returnedResponse["response"] = requests.post(DEFAULT_API_URL + "/todos", json={"title": title})

@when(parsers.parse('the user requests to post a new todo without mandatory field title and with only description "{description}"'))
def post_new_todo_with_invalid_parameter(description, returnedResponse):
    returnedResponse["response"] = requests.post(DEFAULT_API_URL + "/todos", json={"description": description})

@then(parsers.parse('the new todo object with title "{title}", description "{description}", doneStatus "{doneStatus}" as part of projectId "{projectId}" and categoryId "{categoryId}" shall be returned'))
def verify_new_todo_with_all_parameters(title, description, doneStatus, projectId, categoryId, returnedResponse):
    allProjects = requests.get(f'{DEFAULT_API_URL}/projects') 
    sortedProjects = sorted(allProjects.json()['projects'], key=lambda project: project['id'])
    pId = sortedProjects[int(projectId)]['id']
    allCategories = requests.get(f'{DEFAULT_API_URL}/categories') 
    sortedCategories = sorted(allCategories.json()['categories'], key=lambda category: category['id'])
    cId = sortedCategories[int(categoryId)]['id']
    returnData = returnedResponse["response"].json()
    assert returnData["title"] == title
    assert returnData["description"] == description
    assert returnData["doneStatus"] == doneStatus
    assert returnData["tasksof"][0]["id"] == pId
    assert returnData["categories"][0]["id"] == cId
    delete_todo_by_id(returnData['id'])

@then(parsers.parse('the new todo object with title "{title}" shall be returned'))
def verify_new_todo_with_only_title(title, returnedResponse):
    returnData = returnedResponse["response"].json()
    assert returnData["title"] == title
    assert returnData["description"] == ""
    assert returnData["doneStatus"] == "false"
    assert ("tasksof" in returnData) == False
    assert ("categories" in returnData) == False
    delete_todo_by_id(returnData['id'])
    

