"""
Tests for the GET /Books endpoint of the online bookstore API.
These tests validate the structure and uniqueness of book items returned by the API.
"""

import json
import pytest
from tests.schemas import book_schema, common_schemas
from tests.models import book_model, common_models
from tests.api import books_api
from tests.utils import response_validators, data_generators


# --- Helpers & Constants ---

BOOK_ID_AS_STRING = ["abc", "123abc", None, " "] # Invalid book IDs that are not integers.
# These should return 400 Bad Request when used in GET /Books/{id} or POST /Books/{id} endpoints.
# They are not valid integers and should be handled by the API.

BOOK_ID_NOT_VALID_INT = [-1, 0] # Invalid book IDs that are not positive integers.
# These should return 404 Not Found when used in GET /Books/{id} endpoint.

BOOK_NULLABLE_FIELDS = [
    "title",
    "description",
    "excerpt"
]  # Fields that can be nullable in the book model.
# These fields can be omitted when creating or updating a book,
# and the API should handle them gracefully.
# Bad values for required fields that should return 400 Bad Request
# when used in POST or PUT requests.

BOOK_BAD_VALUES = [ # Invalid values for required fields that should return 400 Bad Request
    # when used in POST or PUT requests.
    # These values are not of the expected type or format for the respective fields.
    # Each tuple contains the field name and a bad value that should trigger a validation error.
    ("id", "string_instead_of_int"),
    ("pageCount", "string_instead_of_int"),
    ("publishDate", 12345),  # not a valid date (normally expects string in ISO format)
    ("publishDate", "not-a-date"), # not a valid date
    ("publishDate", "2025-13-01"), # not a valid date
    ("publishDate", "2025-02-30"), # not a valid date
    ("publishDate", "01-01-2025"), # not a valid date
]

# --- Tests for GET /Books Endpoint (list) ---

def test_get_books_validates_all_items(books_api_fixture: books_api.BooksAPI):
    """
    Test to ensure that all items in the GET /Books response
    conform to the expected JSON Schema and Pydantic model.
    This checks both the structure and data types of each book item.
    """
    response = books_api_fixture.get_books()
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")

    books = response.json()
    assert isinstance(books, list), f"Expected list, got {type(books)}"
    assert books, "Books list is empty"

    for idx, item in enumerate(books):
        response_validators.validate_schema_and_model(
            item,
            book_schema.BOOK_SCHEMA,
            book_model.Book,
            idx
        )


def test_get_books_ids_are_unique(books_api_fixture: books_api.BooksAPI):
    """
    Test to ensure that all book IDs in the GET /Books response are unique.
    This checks for duplicate IDs in the list of books returned by the API.
    """
    response = books_api_fixture.get_books()
    books = response.json()
    ids = [b["id"] for b in books]
    assert len(ids) == len(set(ids)), "Duplicate IDs found in books list"


def test_get_books_no_full_duplicates(books_api_fixture: books_api.BooksAPI):
    """
    Test to ensure that no two books in the GET /Books response
    are identical in all fields.
    This checks for full object duplicates in the list of books returned by the API.
    """
    resp = books_api_fixture.get_books()
    books = [json.dumps(b, sort_keys=True) for b in resp.json()]
    assert len(books) == len(set(books)), "Full book object duplicate found"


# NOTE:
# The FakerestAPI demo endpoint is dynamic: on each GET request,
# certain fields such as 'publishDate' are generated with new values.
# This means the API response is not fully idempotent, and full object comparison will fail.
# For the purpose of this test, only static fields (e.g., 'id') are compared.

def test_get_books_is_idempotent(books_api_fixture: books_api.BooksAPI):
    """
    Test to ensure that multiple calls to GET /Books return the same set of books.
    This checks for idempotency by comparing the IDs of books returned in multiple calls.
    """
    first = books_api_fixture.get_books().json()
    second = books_api_fixture.get_books().json()
    # Check only the IDs and length of the lists
    first_ids = [b["id"] for b in first]
    second_ids = [b["id"] for b in second]
    assert first_ids == second_ids, "IDs returned by GET /Books are not idempotent"
    assert len(first) == len(second), "GET /Books returned different number of items"


@pytest.mark.parametrize("method", ["PATCH"])
def test_get_books_wrong_method(books_api_fixture: books_api.BooksAPI, method):
    """
    Test to ensure that using an incorrect HTTP method (e.g., POST) on GET /Books
    returns a 405 Method Not Allowed status code.
    This checks the API's response to unsupported methods.
    """
    response = books_api_fixture.wrong_method(method)
    response_validators.assert_status_code(response, 405)


# --- Tests for GET /Books/{id} Endpoint (single book) ---

def test_get_book_by_id_happy_path(books_api_fixture: books_api.BooksAPI):
    """
    GET /Books/{id} should return a book by its ID and validate the response.
    This checks the successful retrieval of a book by its ID.
    """
    response = books_api_fixture.get_book(1)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        book_schema.BOOK_SCHEMA,
        book_model.Book,
    )


def test_get_book_by_id_not_found(books_api_fixture: books_api.BooksAPI):
    """
    GET /Books/{id} should return 404 Not Found for a book ID that does not exist.
    This checks the API's response when trying to retrieve a book that is not present.
    """
    response = books_api_fixture.get_book(99999)
    response_validators.assert_status_code(response, 404)
    response_validators.assert_json_content_type(
        response,
        "application/problem+json; charset=utf-8; v=1.0"
    )
    response_validators.assert_api_version(response, "1.0")


@pytest.mark.parametrize("book_id", BOOK_ID_NOT_VALID_INT)
def test_get_book_by_id_edge_cases_int_404(books_api_fixture: books_api.BooksAPI, book_id):
    """
    GET /Books/{id} should return 404 Not Found for invalid book IDs (e.g., 0 or negative).
    """
    response = books_api_fixture.get_book(book_id)
    response_validators.assert_status_code(response, 404)
    response_validators.assert_json_content_type(
        response,
        "application/problem+json; charset=utf-8; v=1.0"
    )
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        common_schemas.ERROR_404_SCHEMA,
        common_models.Error404Response
    )


@pytest.mark.parametrize("book_id", BOOK_ID_AS_STRING)
def test_get_book_by_id_edge_cases_str_400(books_api_fixture: books_api.BooksAPI, book_id):
    """
    GET /Books/{id} should return 400 Bad Request for invalid book IDs.
    """
    response = books_api_fixture.get_book(book_id)
    response_validators.assert_status_code(response, 400)
    response_validators.assert_json_content_type(
        response,
        "application/problem+json; charset=utf-8"
    )
    response_validators.validate_schema_and_model(
        response.json(),
        common_schemas.ERROR_400_SCHEMA,
        common_models.Error400Response
    )


# --- Tests for POST /Books Endpoint (add book) ---

def test_post_book_happy_path(books_api_fixture: books_api.BooksAPI):
    """
    POST /Books should allow adding a new book and return the created book data.
    This checks the successful creation of a book."""
    book = data_generators.build_book()
    response = books_api_fixture.add_book(book)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        book_schema.BOOK_SCHEMA,
        book_model.Book
    )


@pytest.mark.parametrize("nullable_field", BOOK_NULLABLE_FIELDS)
def test_post_book_happy_path_with_nullable_fields(
    books_api_fixture: books_api.BooksAPI,
    nullable_field
):
    """
    POST /Books should allow adding a book with nullable fields removed.
    """
    book = data_generators.build_book()
    book.pop(nullable_field)
    response = books_api_fixture.add_book(book)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        book_schema.BOOK_SCHEMA,
        book_model.Book
    )


@pytest.mark.parametrize(
    "field,bad_value", BOOK_BAD_VALUES
)
def test_post_book_400_invalid_type_for_required_fields(books_api_fixture, field, bad_value):
    """
    POST /Books should reject requests with invalid type for required, non-nullable fields.
    """
    book = data_generators.build_book()
    book[field] = bad_value
    response = books_api_fixture.add_book(book)
    response_validators.assert_status_code(response, 400)
    response_validators.assert_json_content_type(
        response,
        "application/problem+json; charset=utf-8"
    )
    response_validators.validate_schema_and_model(
        response.json(),
        common_schemas.ERROR_400_SCHEMA,
        common_models.Error400Response
    )


# --- Tests for PUT /Books/{id} Endpoint (update book) ---

def test_put_book_happy_path(books_api_fixture: books_api.BooksAPI):
    """
    Test to ensure that updating a book by ID returns the updated book data.
    This checks the successful update of a book."""
    book = data_generators.build_book(1)
    response = books_api_fixture.update_book(1, book)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        book_schema.BOOK_SCHEMA,
        book_model.Book
    )

@pytest.mark.parametrize("book_id", BOOK_ID_AS_STRING)
def test_put_book_by_id_edge_cases_str_400(books_api_fixture: books_api.BooksAPI, book_id):
    """
    PUT /Books/{id} should return 400 Bad Request for invalid book IDs.
    """
    book = data_generators.build_book()
    response = books_api_fixture.update_book(book_id, book)
    response_validators.assert_status_code(response, 400)
    response_validators.assert_json_content_type(
        response,
        "application/problem+json; charset=utf-8"
    )
    response_validators.validate_schema_and_model(
        response.json(),
        common_schemas.ERROR_400_SCHEMA,
        common_models.Error400Response
    )


@pytest.mark.parametrize("nullable_field", BOOK_NULLABLE_FIELDS)
def test_put_book_happy_path_with_nullable_fields(
    books_api_fixture: books_api.BooksAPI,
    nullable_field
):
    """
    PUT /Books/{id} should allow updating a book with nullable fields removed.
    """
    book = data_generators.build_book()
    book.pop(nullable_field)
    response = books_api_fixture.update_book(1, book)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        book_schema.BOOK_SCHEMA,
        book_model.Book
    )


@pytest.mark.parametrize(
    "field,bad_value", BOOK_BAD_VALUES
)
def test_put_book_400_invalid_type_for_required_fields(
    books_api_fixture: books_api.BooksAPI,
    field,
    bad_value
):
    """
    PUT /Books/{id} should reject requests with invalid type for required, non-nullable fields.
    """
    book = data_generators.build_book()
    book[field] = bad_value
    response = books_api_fixture.update_book(1, book)
    response_validators.assert_status_code(response, 400)
    response_validators.assert_json_content_type(
        response,
        "application/problem+json; charset=utf-8"
    )
    response_validators.validate_schema_and_model(
        response.json(),
        common_schemas.ERROR_400_SCHEMA,
        common_models.Error400Response
    )


# --- Tests for DELETE /Books/{id} Endpoint (delete book) ---

def test_delete_book_happy_path(books_api_fixture: books_api.BooksAPI):
    """
    Test to ensure that deleting a book by ID returns a 204 No Content status code.
    This checks the successful deletion of a book.
    """
    response = books_api_fixture.delete_book(1)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_header_present(response, "api-supported-versions")
    assert response.content == b'', "Expected no content in response body after deletion"


@pytest.mark.parametrize("book_id", BOOK_ID_AS_STRING)
def test_delete_book_by_id_edge_cases_str_400(books_api_fixture: books_api.BooksAPI, book_id):
    """
    DELETE /Books/{id} should return 400 Bad Request for invalid book IDs.
    """
    response = books_api_fixture.delete_book(book_id)
    response_validators.assert_status_code(response, 400)
    response_validators.assert_json_content_type(
        response,
        "application/problem+json; charset=utf-8"
    )
    response_validators.validate_schema_and_model(
        response.json(),
        common_schemas.ERROR_400_SCHEMA,
        common_models.Error400Response
    )
