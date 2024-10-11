Feature: Edit an existing project 
    As a user, I want to be able to edit an existing project, so that I can update the project details

    Background:
        Given the API is running and responsive
        And the database contains existing projects

    # Normal Flow
    Scenario Outline: Edit an existing project by modifying all fields
        When the user requests to edit an existing project with "<id>" with a new title "<title>", description "<description>", completed "<completed>", and active "<active>"
        Then a status code of "200" shall be returned
        Then the updated project object with title "<title>", description "<description>", completed "<completed>", and active "<active>" shall be returned

        Examples:
            | id | title | description | completed | active |
            | 1  | Project_2 | Modified description  | true | false |
            | 2  | Project_3 |  Also modified description | false | false |

    # Alternate Flow
    Scenario Outline: Edit an existing project by modifying the title only
        When the user requests to edit an existing project with "<id>" with a new title "<title>" only
        Then a status code of "200" shall be returned
        Then the updated project object with title "<title>", description "<description>", completed "<completed>", and active "<active>" shall be returned

        Examples:
            | id | title | description | completed | active |
            | 1  | Yard Renovation Title Updated | Tidy up and freshen up the yard | false | true |
            | 2  | Garage Cleanup Title Updated |  Tidy up and organize the garage | true | false |
            | 3  | Renovate Bathroom Title Updated | Needs a makeover | false | false |
            | 4  | Clean Kitchen Title Updated |  Tidy up and clean the kitchen | true | true |

    # Error Flow
    Scenario Outline: Edit an existing project by providing an invalid field
        When the user requests to edit an existing project with "<id>" with an invalid parameter field "<owner>"
        Then a status code of "400" shall be returned
        And an error "<error>" shall be returned

        Examples:
        | id | owner | error |
        | 1 | Aditya Negi | Could not find field: owner |
        | 2 | Chris Vatos | Could not find field: owner |
        | 3 | Parsa Langari| Could not find field: owner |
        | 4 | Jasmine Taggart | Could not find field: owner |
            

