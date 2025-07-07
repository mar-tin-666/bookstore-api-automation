"""
Common JSON schemas for error responses in the API.
These schemas are used to validate the structure of error responses returned by the API.
"""

ERROR_404_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "title": {"type": "string"},
        "status": {"type": "integer"},
        "traceId": {"type": "string"},
    },
    "required": ["type", "title", "status", "traceId"],
    "additionalProperties": False
}

ERROR_400_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "title": {"type": "string"},
        "status": {"type": "integer"},
        "traceId": {"type": "string"},
        "errors": {
            "type": "object",
            "additionalProperties": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
    },
    "required": ["type", "title", "status", "traceId", "errors"],
    "additionalProperties": False
}
