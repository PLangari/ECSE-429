Feature: Get existing todos
    As a user, I want to be able to get existing todos, so that I can view all my todos

    Background:
        Given the API is running and responsive
        And the database contains existing todos  
    
    # Normal Flow
    Scenario Outline: Get all existing todos
        When the user requests to get all existing todos
        Then a status code of "200" shall be returned
        Then the list of all existing todos shall be returned

    # Alternate Flow
    Scenario Outline: Get all existing todos by a specific doneStatus
        When the user requests to get all existing todos with doneStatus "<doneStatus>"
        Then a status code of "200" shall be returned
        Then a list of all existing todos with doneStatus "<doneStatus>" shall be returned

        Examples:
            | doneStatus |
            | true   |
            | false  |
    
    # Error Flow
    Scenario Outline: Get all existing todos by an invalid parameter
        When the user requests to get all existing todos with an invalid parameter field owner "<owner>"
        Then a status code of "400" shall be returned
        Then an error message shall be returned

        Examples:
            | owner | 
            | Aditya Negi |
            | Chris Vatos |
            | Parsa Langari |
            | Jasmine Taggart |
