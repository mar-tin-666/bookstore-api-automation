"""
Configuration file for pytest.
This file sets up fixtures and configurations for the test suite.
"""

import pytest
from tests.api import books_api, authors_api

@pytest.fixture
def books_api_fixture() -> books_api.BooksAPI:
    """
    Fixture to provide an instance of the BooksAPI client.
    This allows tests to interact with the Books API without needing to instantiate it in each test.
    Returns:
        BooksAPI: An instance of the BooksAPI client.
    """
    return books_api.BooksAPI()


@pytest.fixture
def authors_api_fixture() -> authors_api.AuthorsAPI:
    """
    Fixture to provide an instance of the AuthorsAPI client.
    This allows tests to interact with the Authors API without needing
    to instantiate it in each test.
    Returns:
        AuthorsAPI: An instance of the AuthorsAPI client.
    """
    return authors_api.AuthorsAPI()
