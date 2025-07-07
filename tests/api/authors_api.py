"""
API client for interacting with the Authors endpoint of the online bookstore.
This client provides methods to perform CRUD operations on authors.
"""

import requests
from tests.api import common_api

class AuthorsAPI(common_api.CommonAPI):
    """
    Client for the Authors API.
    This class provides methods to interact with the Authors endpoint of the online bookstore API.
    It includes methods to get all authors, get a single author by ID, add a new author,
    update an existing author, and delete an author.
    """
    def __init__(self):
        """
        Initializes the AuthorsAPI client with the base URL for the Authors endpoint.
        """
        super().__init__()
        self.base_url = self._create_base_url("/api/v1/Authors")

    def get_authors(self, headers=None):
        """
        Fetches the list of all authors from the API.
        Returns:
            Response: The response object containing the list of authors.
        """
        return requests.get(
            url=self.base_url,
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def get_author(self, author_id, headers=None):
        """
        Fetches a single author by its ID from the API.
        """
        return requests.get(
            url=f"{self.base_url}/{author_id}",
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def add_author(self, author_data, headers=None):
        """
        Adds a new author to the API.
        """
        return requests.post(
            url=self.base_url,
            json=author_data,
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def update_author(self, author_id, author_data, headers=None):
        """
        Updates an existing author in the API.
        """
        return requests.put(
            url=f"{self.base_url}/{author_id}",
            json=author_data,
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def delete_author(self, author_id, headers=None):
        """
        Deletes an author from the API.
        """
        return requests.delete(
            url=f"{self.base_url}/{author_id}",
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def wrong_method(self, method_name, author_id=None, headers=None):
        """
        A method that demonstrates an incorrect API call.
        """
        url = self.base_url
        if author_id is not None:
            url = f"{self.base_url}/{author_id}"
        return requests.request(
            method_name,
            url,
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def get_authors_by_book_id(self, id_book, headers=None):
        """
        Fetches all authors associated with a given book ID.
        """
        return requests.get(
            url=f"{self.base_url}/authors/books/{id_book}",
            timeout=self.timeout,
            headers=headers or self.default_headers
        )

    def get_authors_by_book_id_wrong_method(self, method_name, id_book, headers=None):
        """
        A method that demonstrates an incorrect API call for fetching authors by book ID.
        """
        url = f"{self.base_url}/authors/books/{id_book}"
        return requests.request(
            method_name,
            url,
            timeout=self.timeout,
            headers=headers or self.default_headers
        )
