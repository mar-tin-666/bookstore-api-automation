"""
Common JSON schemas for error responses in the API.
These schemas are used to validate the structure of error responses returned by the API.
"""

from typing import Dict, List
from pydantic import BaseModel, Field

class Error404Response(BaseModel):
    """
    Model for error responses from the API.
    This model includes fields for the error type, title, status code, and trace ID.
    """
    type: str = Field(..., description="Type of the error")
    title: str = Field(..., description="Title of the error")
    status: int = Field(..., description="HTTP status code for the error")
    traceId: str = Field(..., description="Trace ID for debugging purposes")

class Error400Response(BaseModel):
    """
    Model for 400 Bad Request error responses from the API.
    This model includes fields for the error type, title, status code, trace ID,
    and a dictionary of validation errors.
    """
    type: str = Field(..., description="Type of the error")
    title: str = Field(..., description="Title of the error")
    status: int = Field(..., description="HTTP status code for the error")
    traceId: str = Field(..., description="Trace ID for debugging purposes")
    errors: Dict[str, List[str]] = Field(..., description="Validation errors")
