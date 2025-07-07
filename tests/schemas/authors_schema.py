"""
Schema for validating Author objects in the API.
This schema is used to ensure that the Author objects returned
by the API conform to the expected structure and data types.
"""

AUTHOR_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "idBook": {"type": "integer"},
        "firstName": {"type": ["string", "null"]},
        "lastName": {"type": ["string", "null"]}
    },
    "required": ["id", "idBook"],
    "additionalProperties": False
}
