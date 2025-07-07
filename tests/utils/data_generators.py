"""
Data generator for creating book instances for testing purposes.
This module provides a function to build a book object with random data using Faker.
"""

from faker import Faker
from tests.models import book_model

def build_book(book_id=None, faker_instance=None):
    """
    Build a book dict with random data.
    Args:
        book_id (int, optional): The ID of the book. If not provided, a random ID will be generated.
        faker_instance (Faker, optional): An instance of Faker to use for generating random data.
            If not provided, a new Faker instance will be created.
    Returns:
        dict: A dictionary representing a book with random data.
    """
    fake = faker_instance or Faker()
    return book_model.Book(
        id=book_id or fake.random_int(min=1, max=10000),
        title=fake.sentence(nb_words=4),
        description=fake.paragraph(),
        pageCount=fake.random_int(min=1, max=1000),
        excerpt=fake.sentence(nb_words=6),
        publishDate=fake.date_time_this_decade().isoformat()
    ).model_dump(mode="json") # Convert to dict for JSON serialization


def build_author(author_id=None, book_id=None, faker_instance=None):
    """
    Build an author dict with random data.
    Args:
        author_id (int, optional): The ID of the author. If not provided,
            a random ID will be generated.
        book_id (int, optional): The ID of the book. If not provided, a random ID will be generated.
        faker_instance (Faker, optional): An instance of Faker to use for generating random data.
            If not provided, a new Faker instance will be created.
    Returns:
        dict: A dictionary representing an author with random data.
    """
    fake = faker_instance or Faker()
    return {
        "id": author_id or fake.random_int(min=1, max=10000),
        "idBook": book_id or fake.random_int(min=1, max=10000),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
    }
