Feature: Get all todo items associated to an existing category 
    As a user, I want to get all todos associated to an existing category, so that I can view what todos need to be accomplished for a category

    Background:
        Given the API is running and responsive
        And the database contains existing categories
        And the database contains existing todos
        And the database contains existing todos associated to existing categories

    Scenario Outline: Get all todos associated to an existing category
        When the user requests to get all todos associated to existing category with id "<categoryId>"
        Then a status code of "200" shall be returned
        Then a list of todos associated to existing category with id "<categoryId>" shall be returned and contain "<numberOfTodos>" todos

        Examples:
            | categoryId | numberOfTodos |
            | 2          | 2 |
            | 3          | 2 |
            | 4          | 0 |
            | 5          | 0 |

    Scenario Outline: Get all todos associated to an existing category with a specific done status
        When the user requests to get all todos associated to existing category with id "<categoryId>" and done status "<doneStatus>"
        Then a status code of "200" shall be returned
        Then a list of todos associated to existing category with id "<categoryId>" and with "<doneStatus>" doneStatus shall be returned and contain "<numberOfTodos>" todos

        Examples: 
            | categoryId | doneStatus | numberOfTodos |
            | 2          | false      | 1 |
            | 3          | true       | 1 |
            | 4          | true       | 0 |
            | 5          | false      | 0 |

    Scenario Outline: Get all todos associated to an invalid/non-existent category 
        When the user requests to get all todos associated to invalid category with id "<categoryId>"
        Then a status code of "404" shall be returned
        And an error "<error>" shall be returned

        Examples:
            | categoryId   | error |
            | invalid_id_1 | Could not find parent thing for relationship categories/invalid_id_1/todos |
            | invalid_id_2 | Could not find parent thing for relationship categories/invalid_id_2/todos |
        