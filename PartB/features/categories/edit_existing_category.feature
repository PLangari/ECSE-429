Feature: Edit an existing category 
    As a user, I want to be able to edit an existing category, so that I can update the category details

    Background:
        Given the API is running and responsive
        And the database contains existing categories

    # Normal Flow
    Scenario Outline: Edit an existing category by modifying all fields
        When the user requests to edit an existing category with "<id>" with a new title "<title>" and description "<description>"
        Then a status code of "200" shall be returned
        Then the updated category object with title "<title>" and description "<description>" shall be returned

        Examples:
            | id | title | description |
            | 2  | Category_2 | Modified description  |
            | 3  | Category_3 |  Also modified description |

    # Alternate Flow
    Scenario Outline: Edit an existing category by modifying the title only
        When the user requests to edit an existing category with "<id>" with a new title "<title>" only
        Then a status code of "200" shall be returned
        Then the updated category object with title "<title>" and description "<description>" shall be returned

        Examples:
            | id | title | description |
            | 2  | Home Title Updated | Tasks related to home |
            | 3  | Work Title Updated |  Tasks related to work |
            | 4  | Personal Title Updated | Personal tasks |
            | 5  | School Title Updated |  Tasks related to school |

    # Error Flow
    Scenario Outline: Edit an existing category by providing an invalid field
        When the user requests to edit an existing category with "<id>" with an invalid parameter field "<owner>"
        Then a status code of "400" shall be returned
        And an error "<error>" shall be returned

        Examples:
        | id | owner | error |
        | 1 | Aditya Negi | Could not find field: owner |
        | 2 | Chris Vatos | Could not find field: owner |
        | 3 | Parsa Langari| Could not find field: owner |
        | 4 | Jasmine Taggart | Could not find field: owner |
