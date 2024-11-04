Feature: Manage project across multiple categories
    As a user, I want to add a project to multiple categories and manage its relationships using the interoperability mechanisms.

    Background:
        Given the API is running and responsive
        And the database contains existing categories and projects

    # Normal Flow
    Scenario Outline: Add a project to multiple categories
        When the user requests to add the project with id "<projectId>" to category with id "<categoryId>"
        Then a status code of "201" shall be returned

        Examples:
            | projectId | categoryId |
            | 1         | 1         |
            | 1         | 2         |
            | 2         | 1         |

    # Alternate Flow
    Scenario Outline: Remove a project from one category while it remains in another
        Given the project with id "<projectId>" is added to categories "<categoryId1>" and "<categoryId2>"
        When the user requests to remove the project with id "<projectId>" from category with id "<categoryId1>"
        Then a status code of "200" shall be returned
        And the project with id "<projectId>" shall still exist in category with id "<categoryId2>"

        Examples:
            | projectId | categoryId1 | categoryId2 |
            | 1         | 1           | 2           |
            | 2         | 1           | 3           |

    # Error Flow
    Scenario Outline: Attempt to add a non-existing project to a category
        When the user requests to add a non-existing project with id "<projectId>" to category with id "<categoryId>"
        Then a status code of "404" shall be returned
        And an error message "<errorMessage>" shall be returned

        Examples:
            | projectId | categoryId | errorMessage                                  |
            | 999       | 1          | Could not find thing matching value for id |
            | 1         | 999        | Could not find parent thing for relationship categories/999/projects |
