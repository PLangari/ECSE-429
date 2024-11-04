Feature: Remove a todo from a project
    As a user, I want to be able to remove a todo from a project using the interoperability mechanisms.

    Background:
        Given the API is running and responsive
        And the database contains existing projects and todos

    # Normal Flow
    Scenario Outline: Remove an existing todo from a project
        When the user requests to remove the todo with id "<todoId>" from project with id "<projectId>"
        Then a status code of "200" shall be returned

        Examples:
            | todoId | projectId |
            | 1      | 1         |
            | 2      | 1         |

    # Alternate Flow
    Scenario Outline: Remove an already removed todo from a project
        Given the todo with id "<todoId>" is already removed from project with id "<projectId>" using /todos/:id/tasksof/:id
        When the user requests to remove the todo with id "<todoId>" from project with id "<projectId>" again using /projects/:id/tasks/:id
        Then a status code of "200" shall be returned

        Examples:
            | todoId | projectId |
            | 1      | 1         |
            | 2      | 1         |

    # Error Flow
    Scenario Outline: Attempt to remove a non-existing todo from a project
        When the user requests to remove a non-existing todo with id "<todoId>" from project with id "<projectId>"
        Then a status code of "404" shall be returned
        And an error message "<errorMessage>" shall be returned

        Examples:
            | todoId | projectId | errorMessage                                                     |
            | 999    | 1         | Could not find any instances with projects/1/tasks/999          |
            | 1      | 999       | Could not find any instances with projects/999/tasks/1          |
