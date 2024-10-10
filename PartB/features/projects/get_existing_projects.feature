Feature: Get existing projects
    As a user, I want to be able to get existing projects, so that I can view what projects are available

    Background:
        Given the API is running and responsive
        And the database contains existing projects 

    # Normal Flow
    Scenario Outline: Get all existing projects
        When the user requests to get all existing projects
        Then a status code of "200" shall be returned
        Then a list of existing projects shall be returned

    # Alternate Flow
    Scenario Outline: Get all existing projects by a specific active status
        When the user requests to get all projects with active status of "<active>"
        Then a status code of "200" shall be returned
        Then a list of existing projects with active status "<active>" shall be returned

        Examples:
            | active |
            | true   |
            | false  |

    # # Error Flow
    Scenario Outline: Get all existing projects by an invalid parameter
        When the user requests to get all existing projects with invalid parameter field owner "<owner>"
        Then a status code of "200" shall be returned
        Then an empty list with no projects shall be returned

        Examples:
            | owner | 
            | Aditya Negi |
            | Chris Vatos |
            | Parsa Langari |
            | Jasmine Taggart |
