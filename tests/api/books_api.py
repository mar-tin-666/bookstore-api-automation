"""
API client for interacting with the Books endpoint of the online bookstore.
This client provides methods to perform CRUD operations on books.
"""

import requests
from tests.api import common_api


class BooksAPI(common_api.CommonAPI):
    """
    Client for the Books API.
    This class provides methods to interact with the Books endpoint of the online bookstore API.
    It includes methods to get all books, get a single book by ID, add a new book,
    update an existing book, and delete a book.
    """
    def __init__(self):
        """
        Initializes the BooksAPI client with the base URL for the Books endpoint.
        """
        super().__init__()
        self.base_url = self._create_base_url("/api/v1/Books")

    def get_books(self, headers=None):
        """
        Fetches the list of all books from the API.
        Returns:
            Response: The response object containing the list of books.
        """
        return requests.get(
            url=self.base_url,
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def get_book(self, book_id, headers=None):
        """
        Fetches a single book by its ID from the API.
        """
        return requests.get(
            url=f"{self.base_url}/{book_id}",
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def add_book(self, book_data, headers=None):
        """
        Adds a new book to the API.
        """
        return requests.post(
            url=self.base_url,
            json=book_data,
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def update_book(self, book_id, book_data, headers=None):
        """
        Updates an existing book in the API.
        """
        return requests.put(
            url=f"{self.base_url}/{book_id}",
            json=book_data,
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def delete_book(self, book_id, headers=None):
        """
        Deletes a book from the API.
        """
        return requests.delete(
            f"{self.base_url}/{book_id}",
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def wrong_method(self, method_name, book_id=None, headers=None):
        """
        A method that demonstrates an incorrect API call.
        """
        return requests.request(
            method_name,
            f"{self.base_url}/{book_id}",
            timeout=self.timeout,
            headers=headers or self.default_headers
        )
