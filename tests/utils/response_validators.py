"""
Utility functions to validate API responses in tests
These functions check the status code, content type, API version, and headers.
"""
import pytest
from jsonschema import validate, ValidationError as JsonSchemaValidationError
from pydantic import ValidationError as PydanticValidationError


def assert_status_code(response, expected_code=200):
    """
    Assert that the response status code matches the expected code.
    Args:
        response: The response object from the API call.
        expected_code: The expected status code (default is 200).
    Raises:
        AssertionError: If the status code does not match the expected code.
    """
    assert response.status_code == expected_code, (
        f"Expected status {expected_code}, got {response.status_code}"
    )


def assert_json_content_type(response, expected_type="application/json; charset=utf-8; v=1.0"):
    """
    Assert that the response content type is JSON.
    Args:
        response: The response object from the API call.
    Raises:
        AssertionError: If the content type is not JSON.
    """
    ct = response.headers.get("content-type", "")
    assert ct.startswith(expected_type), f"Expected content-type {expected_type}, got {ct}"


def assert_api_version(response, expected_version="1.0"):
    """
    Assert that the API response contains the expected API version.
    Args:
        response: The response object from the API call.
        expected_version: The expected API version (default is "1.0").
    Raises:
        AssertionError: If the API version is not as expected.
    """
    versions = response.headers.get("api-supported-versions", "")
    assert expected_version in versions, f"Expected API version {expected_version}, got {versions}"


def assert_header_present(response, header_name):
    """
    Assert that a specific header is present in the response.
    Args:
        response: The response object from the API call.
        header_name: The name of the header to check for.
    Raises:
        AssertionError: If the header is not present.
    """
    assert header_name.lower() in [k.lower() for k in response.headers], (
        f"Header {header_name} missing in response"
    )


def assert_no_extra_headers(response, allowed_headers):
    """
    Assert that no headers are present in the response that are not in the allowed list.
    Args:
        response: The response object from the API call.
        allowed_headers: A list of allowed header names.
    Raises:
        AssertionError: If any unexpected headers are found.
    """
    extra = [k for k in response.headers if k.lower() not in [h.lower() for h in allowed_headers]]
    assert not extra, f"Unexpected headers found: {extra}"


def validate_schema_and_model(item, schema, model, idx=None, label=""):
    """
    Validate an item against a JSON Schema and a Pydantic model.
    Args:
        item: The item to validate.
        schema: The JSON Schema to validate against.
        model: The Pydantic model to validate against.
        idx: The index of the item in a list (if applicable).
        label: A label for the item being validated (for error messages).
    Raises:
        AssertionError: If the item fails validation against the schema or model.
    """
    pos = f" at index {idx}" if idx is not None else ""
    context = f"{label}{pos}".strip()
    # JSON Schema validation
    try:
        validate(instance=item, schema=schema)
    except JsonSchemaValidationError as e:
        pytest.fail(f"{context} failed JSON Schema validation: {e}")
    # Pydantic model validation
    try:
        model(**item)
    except PydanticValidationError as e:
        pytest.fail(f"{context} failed Pydantic model validation: {e}")
