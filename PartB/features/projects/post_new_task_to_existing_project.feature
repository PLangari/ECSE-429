Feature: Creaate a new task for an existing project
    As a user, I want to be able to create a new task for an existing project, so that I can keep track of the tasks that need to be done

    Background:
        Given the API is running and responsive
        And the database contains existing projects

    # Normal Flow
    Scenario Outline: Create a new task for an existing project with all parameter fields filled out
        When the user requests to create a new task with title "<title>", done status "<doneStatus>", and description "<description>" for project with id "<projectId>"
        Then a status code of "201" shall be returned
        Then the created task object with title "<title>", done status "<doneStatus>", and description "<description>" for project with id "<projectId>" shall be returned

        Examples:
            | projectId | title  | doneStatus | description |
            | 1          | New_Task_1 | false       | This is a hard task |
            | 2          | New_Task_2 | true        | This is an easy task |
            | 3          | New_Task_3 | false       | This is a very hard task |
            | 4          | New_Task_4 | true        | This is a very easy task |

    # Alternate Flow
    Scenario Outline: Create a new task for an existing project with all only the title parameter field filled out
        When the user requests to create a new task with title "<title>" for project with id "<projectId>"
        Then a status code of "201" shall be returned
        Then the created task object with title "<title>", done status "<doneStatus>", and description "<description>" for project with id "<projectId>" shall be returned

        Examples:
            | projectId | title  | doneStatus | description |
            | 1          | One of Four Tasks | empty | empty |
            | 2          | Two of Four Tasks | empty | empty |
            | 3          | Three of Four Tasks | empty | empty |
            | 4          | Four of Four Tasks | empty | empty |

    # Error Flow 
    Scenario Outline: Create a new task for a project with an invalid/non-existent project id
        When the user requests to create a new task with title "<title>", done status "<doneStatus>", and description "<description>" for project with invalid id "<projectId>"
        Then a status code of "404" shall be returned
        And an error "<error>" shall be returned

        Examples:
            | projectId | title | doneStatus | description | error |
            | invalid_id_1 | Valid_Task_1 | false | Difficulty unknown | Could not find parent thing for relationship projects/invalid_id_1/tasks |
            | invalid_id_2 | Valid_Task_2 | true | Very easy task | Could not find parent thing for relationship projects/invalid_id_2/tasks |
            