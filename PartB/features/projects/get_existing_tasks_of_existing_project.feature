Feature: Get tasks associated to an existing project 
    As a user, I want to be able to get tasks associated to an existing project, so that I can view what tasks need to be accomplished for a project

    Background:
        Given the API is running and responsive
        And the database contains existing projects
        And the database contains existing tasks associated to existing projects

    Scenario Outline: Get all tasks associated to an existing project
        When the user requests to get all tasks associated to existing project with id "<projectId>"
        Then a status code of "200" shall be returned
        Then a list of tasks associated to existing project with id "<projectId>" shall be returned and contain "<numberOfTasks>" tasks

        Examples:
            | projectId | numberOfTasks |
            | 1         | 2 |
            | 2         | 3 |
            | 3         | 0 |
            | 4         | 0 |

    Scenario Outline: Get all tasks associated to an existing project with a specific done status
        When the user requests to get all tasks associated to existing project with id "<projectId>" and done status "<doneStatus>"
        Then a status code of "200" shall be returned
        Then a list of tasks associated to existing project with id "<projectId>" and with "<doneStatus>" doneStatus shall be returned and contain "<numberOfTasks>" tasks

        Examples: 
            | projectId | doneStatus | numberOfTasks |
            | 1         | false      | 2 |
            | 2         | true       | 2 |
            | 3         | true       | 0 |
            | 4         | false      | 0 |

    Scenario Outline: Get all tasks associated to an invalid/non-existent project 
        When the user requests to get all tasks associated to invalid project with id "<projectId>"
        Then a status code of "404" shall be returned
        And an error "<error>" shall be returned

        Examples:
            | projectId | error |
            | invalid_id_1 | Could not find parent thing for relationship projects/invalid_id_1/tasks |
            | invalid_id_2 | Could not find parent thing for relationship projects/invalid_id_2/tasks |
        