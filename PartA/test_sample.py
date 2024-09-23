import requests

# Reference for running endpoint tests
def test_create_todo():
    url = "http://localhost:4567/todos"  
    new_book = {"title": "The Hobbit", "doneStatus": False, "description": "In a hole in the ground there lived a hobbit."}
    response = requests.post(url, json=new_book)

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"

    # Check if the book was created (specifics depend on your mock API's response)
    data = response.json()
    assert "id" in data 
    assert data["title"] == "The Hobbit"
    assert data["description"] == "In a hole in the ground there lived a hobbit."