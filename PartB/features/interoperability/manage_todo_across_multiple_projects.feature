Feature: Manage a todo across multiple projects
    As a user, I want to be able to manage a single todo across multiple projects to track it across different scopes.

    Background:
        Given the API is running and responsive
        And the database contains existing projects and todos

    # Normal Flow
    Scenario Outline: Add an existing todo to multiple projects
        When the user adds the todo with id "<todoId>" to the project with id "<projectId>"
        Then a status code of "201" shall be returned

        Examples:
            | todoId | projectId |
            | 1      | 1         |
            | 1      | 2         |

    # Alternate Flow
    Scenario Outline: Remove a todo from one project while it remains in another
        Given the todo with id "<todoId>" is associated with the project with id "<projectId>"
        When the user requests to remove the todo with id "<todoId>" from project with id "<projectIdToRemove>"
        Then a status code of "200" shall be returned
        And the todo with id "<todoId>" should still be associated with project with id "<remainingProjectId>"

        Examples:
            | todoId | projectId | projectIdToRemove | remainingProjectId |
            | 1      | 1         | 1                 | 2                  |

    # Error Flow
    Scenario Outline: Attempt to add a non-existing todo to a project
        When the user tries to add a non-existing todo with id "<invalidTodoId>" to project with id "<projectId>"
        Then a status code of "404" shall be returned
        And an error message "<errorMessage>" shall be returned

        Examples:
            | invalidTodoId | projectId | errorMessage                                          |
            | 999           | 1         | Could not find thing matching value for id  |
            | 1             | 999       | Could not find parent thing for relationship projects/999/tasks |
