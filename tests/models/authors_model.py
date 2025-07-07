"""
Model for Author in the online bookstore API.
This model defines the structure of an Author object,
including its fields and their types.
"""
from pydantic import BaseModel, Field

class Author(BaseModel):
    """
    Represents an author in the online bookstore API.
    """
    id: int = Field(..., ge=1)
    idBook: int = Field(..., ge=1)
    firstName: str | None = None
    lastName: str | None = None
