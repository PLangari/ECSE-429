Feature: Post new category
    As a user, I want to create a new category, so that I can categorize my todos and projects

    Background: 
        Given the API is running and responsive

    # Normal Flow
    Scenario Outline: Successfully create a new category with a title and description
        When a new category is created with title "<title>" and description "<description>"
        Then a status code of "201" shall be returned
        And the created category object with title "<title>" and description "<description>" shall be returned

    Examples:
        | title | description |
        | New_Category_1 | New Category #1 |
        | New_Category_2 | New Category #2 |

    # Alternate Flow 
    Scenario Outline: Create a new category with only title field filled out
        When a new category is created with title "<title>"
        Then a status code of "201" shall be returned
        And the created category object with title "<title>" and description "<description>" shall be returned

    Examples:
        | title | description |
        | New_Category_3 | empty |
        | New_Category_4 | empty |

    # Error Flow 
    Scenario Outline: Create a new category without a title
         When a new category is created without a title and with only description "<description>"
         Then a status code of "400" shall be returned
         And an error "<error>" shall be returned

    Examples:
        | description | error |
        | New Category #5 | title : field is mandatory |
        | New Category #6 | title : field is mandatory |


