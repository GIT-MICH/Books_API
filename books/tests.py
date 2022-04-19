from django.test import TestCase
import pytest

from django.test import Client
from django.urls import reverse

from books.forms import BookForm, BookModifyForm, ImportBooksFromApiForm
from books.models import Book


@pytest.mark.django_db
def test_all_books_view():
    client = Client()
    url = reverse('books-all')
    response = client.get(url)
    assert response.status_code == 200
    assert Book.objects.count() == 0


@pytest.mark.django_db
def test_add_book_view_get():
    client = Client()
    url = reverse('book-add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], BookForm)


@pytest.mark.django_db
def test_add_book_view_post(data):
    client = Client()
    url = reverse('book-add')
    response = client.post(url, data)
    assert Book.objects.count() == 1
    assert response.status_code == 302
    new_url = reverse('books-all')
    assert response.url.startswith(new_url)
    Book.objects.get(title='some title')


@pytest.mark.django_db
def test_delete_book_view(some_id, book):
    client = Client()
    url = reverse('book-delete', args=(some_id,))
    response = client.get(url)
    assert Book.objects.count() == 0
    assert response.status_code == 302
    new_url = reverse('books-all')
    assert response.url.startswith(new_url)


@pytest.mark.django_db
def test_modify_book_view_get(some_id, book):
    client = Client()
    url = reverse('book-modify', args=(some_id,))
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], BookModifyForm)


@pytest.mark.django_db
def test_modify_book_view_post(some_id, book, data):
    client = Client()
    url = reverse('book-modify', args=(some_id,))
    response = client.get(url)
    response = client.post(url, data)
    assert Book.objects.count() == 1
    assert response.status_code == 302
    new_url = reverse('books-all')
    assert response.url.startswith(new_url)


@pytest.mark.django_db
def test_search_books_view_get():
    client = Client()
    url = reverse('books-search')
    response = client.get(url)
    assert response.status_code == 200
    assert Book.objects.count() == 0


@pytest.mark.django_db
def test_search_books_view_post(data):
    client = Client()
    url = reverse('books-search')
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_import_books_view_get():
    client = Client()
    url = reverse('books-import')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ImportBooksFromApiForm)


@pytest.mark.django_db
def test_import_books_view_post():
    client = Client()
    url = reverse('books-import')
    data = {
        'title': 'some title',
        'author': 'some author',
        'publisher': 'publisher',
        'isbn': '1234512345123',
        'subject': 'subject',
        'lccn': 'lccn',
        'oclc': 'oclc'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 302
    new_url = reverse('books-all')
    assert response.url.startswith(new_url)


@pytest.mark.django_db
def test_book_list_view():
    client = Client()
    url = reverse('book-api')
    response = client.get(url)
    assert response.status_code == 200
    assert Book.objects.count() == len(response.data)
