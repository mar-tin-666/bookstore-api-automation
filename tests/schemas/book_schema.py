"""
Schema for validating book data in the online bookstore API.
This schema defines the structure and data types for book objects returned by the API.
It is used to ensure that the book data conforms to the expected format.
"""

BOOK_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": ["string", "null"]},
        "description": {"type": ["string", "null"]},
        "pageCount": {"type": "integer"},
        "excerpt": {"type": ["string", "null"]},
        "publishDate": {"type": "string", "format": "date-time"},
    },
    "required": [
        "id",
        "title",
        "description",
        "pageCount",
        "excerpt",
        "publishDate"
    ],
    "additionalProperties": False
}
