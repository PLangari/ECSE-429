import requests
from utils.default_variables import DEFAULT_API_URL

def populate_todos(num_todos):
    for i in range(num_todos):
        requests.post(f'{DEFAULT_API_URL}/todos', json={"title": f"todo{i}", "description": f"description{i}", "doneStatus": False})


def delete_all_todos():
    allTodos = requests.get(f'{DEFAULT_API_URL}/todos')
    for todo in allTodos.json()['todos']:
        requests.delete(f'{DEFAULT_API_URL}/todos/{todo["id"]}')