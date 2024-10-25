Feature: Add a todo to a project
    As a user, I want to be able to add an existing todo to a project, so that I can manage my todos

    Background: 
        Given the API is running and responsive
        And the database contains existing todos
        And the database contains existing projects

    # Normal Flow
    Scenario Outline: Add an existing todo to an existing project
        When the user requests to add an existing todo "<todoId>" to an existing project "<projectId>"
        Then a status code of "201" shall be returned

        Examples:
            | todoId | projectId |
            | 1  | 1 |
            | 2  | 2 |


    # Alternate Flow
    Scenario Outline: Create a new project for the todo
        When the user requests to add an existing todo "<todoId>" to a new project "<projectName>"
        Then a status code of "201" shall be returned
        And the new project object "<projectName>" shall be returned 

        Examples:
            | todoId | projectName |
            | 1  | New project 1 |
            | 2  | New project 2 |

    # Error Flow
    Scenario Outline: Add a todo to a nonexisting project
        When the user requests to add an existing todo "<todoId>" to a nonexisting project "<projectId>"
        Then a status code of "404" shall be returned
        And an error "<error>" shall be returned

        Examples:
            | todoId | projectId | error |
            | 1  | -100 | Could not find thing matching value for id |
            | 2  | -200 | Could not find thing matching value for id |