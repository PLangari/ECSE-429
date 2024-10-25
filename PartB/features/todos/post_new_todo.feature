Feature: Post new todo
    As a user, I want to create a new todo, so that I can manage my todos

    Background: 
        Given the API is running and responsive
        Given the database contains existing projects
        Given the database contains existing categories

    # Normal Flow
    Scenario Outline: Post a new todo with all parameter fields filled out
        When the user requests to post a new todo with title "<title>", description "<description>", doneStatus "<doneStatus>" as part of projectId "<projectId>" and categoryId "<categoryId>"
        Then a status code of "201" shall be returned
        And the new todo object with title "<title>", description "<description>", doneStatus "<doneStatus>" as part of projectId "<projectId>" and categoryId "<categoryId>" shall be returned

        Examples:
            | title | description | doneStatus | projectId | categoryId |
            | Todo_1 | Description 1 | true | 1 | 1 |
            | Todo_2 | Description 2 | false | 2 | 2 |
            | Todo_3 | Description 3 | true | 3 | 3 |
            | Todo_4 | Description 4 | false | 4 | 4 |

    # Alternate Flow
    Scenario Outline: Post a new todo with only the title field filled out
        When the user requests to post a new todo with title "<title>" only
        Then a status code of "201" shall be returned
        And the new todo object with title "<title>" shall be returned

        Examples:
            | title |
            | Todo_1 |
            | Todo_2 |
            | Todo_3 |
            | Todo_4 |

    # Error Flow
    Scenario Outline: Post a new todo without a title
        When the user requests to post a new todo without mandatory field title and with only description "<description>"
        Then a status code of "400" shall be returned
        And an error "<error>" shall be returned

        Examples:
            | description | error |
            | Description 1 | title : field is mandatory |
            | Description 2 | title : field is mandatory |
            | Description 3 | title : field is mandatory |
            | Description 4 | title : field is mandatory |
            


