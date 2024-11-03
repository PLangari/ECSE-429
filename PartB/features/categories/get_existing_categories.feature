Feature: Get existing categories
    As a user, I want to be able to get all existing categories, so that I can view what categories are available

    Background:
        Given the API is running and responsive
        And the database contains existing categories

    # Normal Flow
    Scenario Outline: Get all existing categories
        When the user requests to get all existing categories
        Then a status code of "200" shall be returned
        And a list of existing categories shall be returned

    # Alternate Flow
    Scenario Outline: Get all existing categories by a specific title
        When the user requests to get all categories with title "<title>"
        Then a status code of "200" shall be returned
        And a list of existing categories with title "<title>" shall be returned

        Examples:
            | title  |
            | School |
            | Work   |

    # Error Flow
    Scenario Outline: Get all existing categories by an invalid parameter
        When the user requests to get all existing categories with invalid parameter field owner "<owner>"
        Then a status code of "200" shall be returned
        And an empty list with no categories shall be returned

        Examples:
            | owner | 
            | Aditya Negi |
            | Chris Vatos |
            | Parsa Langari |
            | Jasmine Taggart |
