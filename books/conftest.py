import pytest

from books.models import Book


@pytest.fixture
def some_id():
    for i in range(1, 3):
        return str(i)


@pytest.fixture
def book(some_id):
    return Book.objects.create(pk=some_id)


@pytest.fixture
def data():
    data = {
        'title': 'some title',
        'author': 'some author',
        'publicate_year': 2022,
        'number_of_pages': 15,
        'isbn_number': '1234512345123',
        'publicate_language': 'pl'
    }
    return data
