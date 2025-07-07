"""
Tests for the /Authors endpoint of the online bookstore API.
"""

import json
import pytest
from tests.schemas import authors_schema, common_schemas
from tests.models import authors_model, common_models
from tests.api import authors_api
from tests.utils import response_validators, data_generators

# --- Helpers & Constants ---

AUTHOR_ID_AS_STRING = ["abc", "123abc", None, " "] # Invalid author IDs that are not integers
AUTHOR_ID_NOT_VALID_INT = [-1, 0] # Invalid author IDs that are not positive integers
AUTHOR_NULLABLE_FIELDS = ["firstName", "lastName"] # Fields that can be omitted in POST/PUT requests
AUTHOR_BAD_VALUES = [ # Invalid values for required fields in POST/PUT requests
    ("id", "string_instead_of_int"),
    ("idBook", "string_instead_of_int"),
    ("firstName", 12345),
    ("lastName", 12345),
]
AUTHOR_WRONG_METHODS = ["PATCH"] # Methods that should not be allowed on /Authors endpoint
# These methods should return 405 Method Not Allowed

AUTHOR_BOOKS_ID_AS_STRING = ["abc", "123abc", None, " "] # Invalid book IDs that are not integers
AUTHOR_BOOKS_WRONG_METHODS = [
    "POST",
    "PUT",
    "DELETE",
    "PATCH"
] # Methods that should not be allowed on /Authors/{id}/Books endpoint


# --- Tests for GET /Authors Endpoint (list) ---

def test_get_authors_validates_all_items(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests that the API returns a list of authors with valid schema and model.
    This test checks that each author in the list conforms to the expected schema and model."""
    response = authors_api_fixture.get_authors()
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")

    authors = response.json()
    assert isinstance(authors, list), f"Expected list, got {type(authors)}"
    assert authors, "Authors list is empty"

    for idx, item in enumerate(authors):
        response_validators.validate_schema_and_model(
            item,
            authors_schema.AUTHOR_SCHEMA,
            authors_model.Author,
            idx
        )


def test_get_authors_ids_are_unique(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests that the API returns a list of authors with unique IDs.
    """
    response = authors_api_fixture.get_authors()
    authors = response.json()
    ids = [a["id"] for a in authors]
    assert len(ids) == len(set(ids)), "Duplicate IDs found in authors list"


def test_get_authors_no_full_duplicates(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests that the API does not return full duplicate author objects.
    """
    resp = authors_api_fixture.get_authors()
    authors = [json.dumps(a, sort_keys=True) for a in resp.json()]
    assert len(authors) == len(set(authors)), "Full author object duplicate found"


@pytest.mark.parametrize("method", AUTHOR_WRONG_METHODS)
def test_authors_wrong_method(authors_api_fixture: authors_api.AuthorsAPI, method):
    """
    Tests that the API returns a 405 Method Not Allowed for incorrect methods on /Authors.
    """
    response = authors_api_fixture.wrong_method(method)
    response_validators.assert_status_code(response, 405)


# --- Tests for GET /Authors/{id} Endpoint (single author) ---

def test_get_author_by_id_happy_path(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests the happy path for fetching an author by ID.
    """
    response = authors_api_fixture.get_author(1)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        authors_schema.AUTHOR_SCHEMA,
        authors_model.Author,
    )


def test_get_author_by_id_not_found(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests that GET /Authors/{id} returns 404 Not Found for non-existent author IDs.
    """
    response = authors_api_fixture.get_author(99999)
    response_validators.assert_status_code(response, 404)
    response_validators.assert_json_content_type(
        response, "application/problem+json; charset=utf-8; v=1.0"
    )
    response_validators.assert_api_version(response, "1.0")


@pytest.mark.parametrize("author_id", AUTHOR_ID_NOT_VALID_INT)
def test_get_author_by_id_edge_cases_int_404(
    authors_api_fixture: authors_api.AuthorsAPI,
    author_id
):
    """
    Tests that GET /Authors/{id} returns 404 Not Found for invalid author IDs.
    """
    response = authors_api_fixture.get_author(author_id)
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


@pytest.mark.parametrize("author_id", AUTHOR_ID_AS_STRING)
def test_get_author_by_id_edge_cases_str_400(
    authors_api_fixture: authors_api.AuthorsAPI,
    author_id
):
    """
    Tests that GET /Authors/{id} returns 400 Bad Request for invalid author ID formats.
    """
    response = authors_api_fixture.get_author(author_id)
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

# --- Tests for POST /Authors Endpoint (add author) ---

def test_post_author_happy_path(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests the happy path for adding a new author.
    """
    author = data_generators.build_author()
    response = authors_api_fixture.add_author(author)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        authors_schema.AUTHOR_SCHEMA,
        authors_model.Author
    )

@pytest.mark.parametrize("nullable_field", AUTHOR_NULLABLE_FIELDS)
def test_post_author_happy_path_with_nullable_fields(
    authors_api_fixture: authors_api.AuthorsAPI,
    nullable_field
):
    """
    Tests that POST /Authors accepts requests with nullable fields omitted.
    """
    author = data_generators.build_author()
    author.pop(nullable_field)
    response = authors_api_fixture.add_author(author)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        authors_schema.AUTHOR_SCHEMA,
        authors_model.Author
    )

@pytest.mark.parametrize("field,bad_value", AUTHOR_BAD_VALUES)
def test_post_author_400_invalid_type_for_required_fields(authors_api_fixture, field, bad_value):
    """
    Tests that POST /Authors rejects requests with invalid type for required, non-null fields.
    """
    author = data_generators.build_author()
    author[field] = bad_value
    response = authors_api_fixture.add_author(author)
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

# --- Tests for PUT /Authors/{id} Endpoint (update author) ---

def test_put_author_happy_path(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests the happy path for updating an author by ID.
    """
    author = data_generators.build_author(1)
    response = authors_api_fixture.update_author(1, author)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        authors_schema.AUTHOR_SCHEMA,
        authors_model.Author
    )

@pytest.mark.parametrize("author_id", AUTHOR_ID_AS_STRING)
def test_put_author_by_id_edge_cases_str_400(
    authors_api_fixture: authors_api.AuthorsAPI,
    author_id
):
    """
    Tests that PUT /Authors/{id} returns 400 Bad Request for invalid author ID formats.
    """
    author = data_generators.build_author()
    response = authors_api_fixture.update_author(author_id, author)
    response_validators.assert_status_code(response, 400)
    response_validators.assert_json_content_type(
        response, "application/problem+json; charset=utf-8"
    )
    response_validators.validate_schema_and_model(
        response.json(),
        common_schemas.ERROR_400_SCHEMA,
        common_models.Error400Response
    )

@pytest.mark.parametrize("nullable_field", AUTHOR_NULLABLE_FIELDS)
def test_put_author_happy_path_with_nullable_fields(
    authors_api_fixture: authors_api.AuthorsAPI,
    nullable_field
):
    """
    Tests that PUT /Authors/{id} accepts requests with nullable fields omitted.
    """
    author = data_generators.build_author()
    author.pop(nullable_field)
    response = authors_api_fixture.update_author(1, author)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")
    response_validators.validate_schema_and_model(
        response.json(),
        authors_schema.AUTHOR_SCHEMA,
        authors_model.Author
    )

@pytest.mark.parametrize("field,bad_value", AUTHOR_BAD_VALUES)
def test_put_author_400_invalid_type_for_required_fields(
    authors_api_fixture: authors_api.AuthorsAPI,
    field, bad_value
):
    """
    Tests that PUT /Authors/{id} rejects requests with invalid type for required,
    non-null fields.
    """
    author = data_generators.build_author()
    author[field] = bad_value
    response = authors_api_fixture.update_author(1, author)
    response_validators.assert_status_code(response, 400)
    response_validators.assert_json_content_type(
        response, "application/problem+json; charset=utf-8"
    )
    response_validators.validate_schema_and_model(
        response.json(),
        common_schemas.ERROR_400_SCHEMA,
        common_models.Error400Response
    )


# --- Tests for DELETE /Authors/{id} Endpoint (delete author) ---

def test_delete_author_happy_path(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests the happy path for deleting an author by ID.
    """
    response = authors_api_fixture.delete_author(1)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_header_present(response, "api-supported-versions")
    assert response.content == b'', "Expected no content in response body after deletion"


@pytest.mark.parametrize("author_id", AUTHOR_ID_AS_STRING)
def test_delete_author_by_id_edge_cases_str_400(
    authors_api_fixture: authors_api.AuthorsAPI,
    author_id
):
    """
    Tests that the API returns a 400 Bad Request for invalid author ID formats.
    """
    response = authors_api_fixture.delete_author(author_id)
    response_validators.assert_status_code(response, 400)
    response_validators.assert_json_content_type(
        response, "application/problem+json; charset=utf-8"
    )
    response_validators.validate_schema_and_model(
        response.json(),
        common_schemas.ERROR_400_SCHEMA,
        common_models.Error400Response
    )


# -- Tests for GET /Authors/authors/books/{idBook} ---

def test_get_authors_by_book_id_happy_path(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests the happy path for fetching authors by book ID.
    """
    response = authors_api_fixture.get_authors_by_book_id(1)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")

    authors = response.json()
    assert isinstance(authors, list), f"Expected list, got {type(authors)}"
    assert authors, "Authors list is empty"

    for idx, item in enumerate(authors):
        response_validators.validate_schema_and_model(
            item,
            authors_schema.AUTHOR_SCHEMA,
            authors_model.Author,
            idx
        )

def test_get_authors_by_book_id_empty_list(authors_api_fixture: authors_api.AuthorsAPI):
    """
    Tests the case where no authors are found for a given book ID.
    """
    response = authors_api_fixture.get_authors_by_book_id(99999)
    response_validators.assert_status_code(response, 200)
    response_validators.assert_json_content_type(response)
    response_validators.assert_api_version(response, "1.0")

    authors = response.json()
    assert isinstance(authors, list), f"Expected list, got {type(authors)}"
    assert not authors, "Expected empty list for non-existent book ID"


@pytest.mark.parametrize("book_id", AUTHOR_BOOKS_ID_AS_STRING)
def test_get_authors_by_book_id_edge_cases_str_400(
    authors_api_fixture: authors_api.AuthorsAPI,
    book_id
):
    """
    Tests that the API returns a 400 Bad Request for invalid book ID formats.
    """
    response = authors_api_fixture.get_authors_by_book_id(book_id)
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

@pytest.mark.parametrize("method", AUTHOR_BOOKS_WRONG_METHODS)
def test_authors_books_wrong_method(authors_api_fixture: authors_api.AuthorsAPI, method):
    """
    Tests that the API returns a 405 Method Not Allowed
    for incorrect methods on /Authors/authors/books/{idBook}.
    """
    response = authors_api_fixture.get_authors_by_book_id_wrong_method(method, 1)
    response_validators.assert_status_code(response, 405)
