import pytest
from utils.todos_utils import *

# Setup
@pytest.fixture
def add_todos_to_database_and_cleanup():
    id_of_new_todo_1 = create_new_todo(new_todo_title_1, new_todo_doneStatus_1, new_todo_description_1)
    id_of_new_todo_2 = create_new_todo(new_todo_title_2, new_todo_doneStatus_2, new_todo_description_2)
    yield
    delete_todo_by_id(id_of_new_todo_1)
    delete_todo_by_id(id_of_new_todo_2)