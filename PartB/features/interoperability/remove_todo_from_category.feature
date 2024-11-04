Feature: Remove a todo from a category
    As a user, I want to be able to remove a todo from a category using the interoperability mechanisms.

    Background:
        Given the API is running and responsive
        And the database contains existing categories and todos

    # Normal Flow
    Scenario Outline: Remove an existing todo from a category
        When the user requests to remove the todo with id "<todoId>" from category with id "<categoryId>"
        Then a status code of "200" shall be returned

        Examples:
            | todoId | categoryId |
            | 1      | 1         |
            | 2      | 1         |

    # Alternate Flow
    Scenario Outline: Remove an already removed todo from a category
        Given the todo with id "<todoId>" is already removed from category with id "<categoryId>"
        When the user requests to remove the todo with id "<todoId>" from category with id "<categoryId>" again
        Then a status code of "200" shall be returned

        Examples:
            | todoId | categoryId |
            | 1      | 1         |
            | 2      | 1         |

    # Error Flow
    Scenario Outline: Attempt to remove a non-existing todo from a category
        When the user requests to remove a non-existing todo with id "<todoId>" from category with id "<categoryId>"
        Then a status code of "404" shall be returned
        And an error message "<errorMessage>" shall be returned

        Examples:
            | todoId | categoryId | errorMessage                                                     |
            | 999    | 1         | Could not find any instances with categories/1/todos/999         |
            | 1      | 999       | Could not find any instances with categories/999/todos/1         |
