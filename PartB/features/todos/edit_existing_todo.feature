Feature: Edit an existing todo 
    As a user, I want to be able to edit an existing todo, so that I can update the todo details

    Background: 
        Given the API is running and responsive
        And the database contains existing todos

    # Normal Flow
    Scenario Outline: Edit an existing todo by modifying all fields
        When the user requests to edit an existing todo with "<id>" with a new title "<title>", description "<description>", doneStatus "<doneStatus>"
        Then a status code of "200" shall be returned
        Then the updated todo object with title "<title>", description "<description>", and doneStatus "<doneStatus>" shall be returned

        Examples:
            | id | title | description | doneStatus |
            | 1  | Todo_2 | Modified description  | true |
            | 2  | Todo_3 |  Also modified description | false |

    # Alternate Flow
    Scenario Outline: Edit an existing todo by modifying the title only
        When the user requests to edit an existing todo with "<id>" with a new title "<title>" only
        Then a status code of "200" shall be returned
        Then the updated todo object with title "<title>", description "<description>", and doneStatus "<doneStatus>" shall be returned

        Examples:
            | id | title | description | doneStatus |
            | 1  | Todo_2 |  empty | empty |
            | 2  | Todo_3 |  empty | empty |

    # Error Flow
    Scenario Outline: Edit an existing todo by providing an invalid field
        When the user requests to edit an existing todo with "<id>" with an invalid parameter field "<owner>"
        Then a status code of "400" shall be returned
        And an error "<error>" shall be returned

        Examples:
        | id | owner | error |
        | 1 | Aditya Negi | Could not find field: owner |
        | 2 | Chris Vatos | Could not find field: owner |
        | 3 | Parsa Langari| Could not find field: owner |
        | 4 | Jasmine Taggart | Could not find field: owner |
