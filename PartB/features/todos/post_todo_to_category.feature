Feature: Add a todo to a category
    As a user, I want to be able to add an existing todo to a category, so that I can manage my todos

    Background: 
        Given the API is running and responsive
        And the database contains existing todos
        And the database contains existing categories

    # Normal Flow
    Scenario Outline: Add an existing todo to an existing category
        When the user requests to add an existing todo "<todoId>" to an existing category "<categoryId>"
        Then a status code of "201" shall be returned

        Examples:
            | todoId | categoryId |
            | 1  | 1 |
            | 2  | 2 |


    # Alternate Flow
    Scenario Outline: Create a new category for the todo
        When the user requests to add an existing todo "<todoId>" to a new category "<categoryName>"
        Then a status code of "201" shall be returned
        And the new category object "<categoryName>" shall be returned 

        Examples:
            | todoId | categoryName |
            | 1  | New Category 1 |
            | 2  | New Category 2 |

    # Error Flow
    Scenario Outline: Add a todo to a nonexisting category
        When the user requests to add an existing todo "<todoId>" to a nonexisting category "<categoryId>"
        Then a status code of "404" shall be returned
        And an error "<error>" shall be returned

        Examples:
            | todoId | categoryId | error |
            | 1  | -100 | Could not find thing matching value for id |
            | 2  | -200 | Could not find thing matching value for id |