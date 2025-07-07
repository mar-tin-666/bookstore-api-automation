"""
Model for Book in the online bookstore API.
This model defines the structure and data types for book objects.
It is used to ensure that the book data conforms to the expected format.
"""

from datetime import datetime
from pydantic import BaseModel, Field

class Book(BaseModel):
    """
    Model representing a book in the online bookstore API.
    This model includes fields for the book's ID, title, description, page count,
    excerpt, and publish date.
    """
    id: int = Field(default=0, description="Unique identifier for the book")
    title: str | None = Field(default=None, description="Title of the book")
    description: str | None = Field(default=None, description="Description of the book")
    pageCount: int = Field(default=0, description="Number of pages in the book")
    excerpt: str | None = Field(default=None, description="Excerpt of the book")
    publishDate: datetime = Field(
        default_factory=datetime.now,
        description="Publish date of the book"
    )
