Feature: Post new project
    As a user, I want to create a new project, so that I can manage my projects

    Background: 
        Given the API is running and responsive

    # Normal Flow
    Scenario Outline: Post a new project with all parameter fields filled out
        When the user wants to post a new project with title "<title>", description "<description>", completed "<completed>", and active "<active>"
        Then a status code of "201" shall be returned
        Then the created project object with title "<title>", description "<description>", completed "<completed>", and active "<active>" shall be returned

    Examples:
        | title | description | completed | active |
        | New_Project_1 | New Project #1 | false | true |
        | New_Project_2 | New Project #2 | true | false |

    # Alternate Flow 
    Scenario Outline: Post a new project with only title field filled out
        When the user wants to post a new project with title "<title>"
        Then a status code of "201" shall be returned
        Then the created project object with title "<title>", description "<description>", completed "<completed>", and active "<active>" shall be returned

    Examples:
        | title | description | completed | active |
        | New_Project_3 | empty | false | false |
        | New_Project_4 | empty | false | false |

    # # Error Flow 
    Scenario Outline: Post a new project with an invalid parameter field
         When the user wants to post a new project with invalid field owner "<owner>"
         Then a status code of "400" shall be returned
         And an error "<error>" shall be returned

    Examples:
        | owner | error |
        | Aditya Negi | Could not find field: owner |
        | Chris Vatos | Could not find field: owner |
        | Parsa Langari| Could not find field: owner |
        | Jasmine Taggart | Could not find field: owner |


