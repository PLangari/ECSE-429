Feature: Remove a project from a category
    As a user, I want to be able to remove a project from a category using the interoperability mechanisms.

    Background:
        Given the API is running and responsive
        And the database contains existing categories and projects

    # Normal Flow
    Scenario Outline: Remove an existing project from a category
        When the user requests to remove the project with id "<projectId>" from category with id "<categoryId>"
        Then a status code of "200" shall be returned

        Examples:
            | projectId | categoryId |
            | 1         | 1         |
            | 2         | 1         |

    # Alternate Flow
    Scenario Outline: Remove an already removed project from a category
        Given the project with id "<projectId>" is already removed from category with id "<categoryId>"
        When the user requests to remove the project with id "<projectId>" from category with id "<categoryId>" again
        Then a status code of "200" shall be returned

        Examples:
            | projectId | categoryId |
            | 1         | 1         |
            | 2         | 1         |

    # Error Flow
    Scenario Outline: Attempt to remove a non-existing project from a category
        When the user requests to remove a non-existing project with id "<projectId>" from category with id "<categoryId>"
        Then a status code of "404" shall be returned
        And an error message "<errorMessage>" shall be returned

        Examples:
            | projectId | categoryId | errorMessage                                                     |
            | 999       | 1         | Could not find any instances with categories/1/projects/999      |
            | 1         | 999       | Could not find any instances with categories/999/projects/1      |
