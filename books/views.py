import requests
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from books.forms import BookModelForm
from books.models import Book
from books.serializers import BookSerializer
from rest_framework import generics


def get_books_from_googleapi(request, url='https://www.googleapis.com/books/v1/volumes?q=Hobbit'):
    """ Get books from // googleapis.com // and save records to database"""
    response = requests.get(url)
    data = response.json()
    items = data.get('items')
    if items is None:
        items = []
    for item in items:
        book = item.get('volumeInfo')
        title = book.get('title', '-')
        authors = book.get('authors', ['no data'])[0]
        # if authors:
        #     author = authors[0]
        publicate_year = book.get('publishedDate')[:4]
        isbns = book.get('industryIdentifiers')
        isbn = isbns[0]['identifier']
        # isbn = None
        # for isbn in isbns:
        #     if isbn['type'] == 'ISBN10':
        #         isbn = isbn['identifier']
        #     elif isbn['type'] == 'ISBN13':
        #         isbn = isbn['identifier']
        number_of_pages = book.get('pageCount')
        publicate_language = book.get('language')
        image = book.get('imageLinks')
        if image:
            image = image.get('thumbnail')
        try:
            book = get_object_or_404(
                Book, title=title, author=authors, publicate_year=publicate_year,
                number_of_pages=number_of_pages, image=image, isbn_number=isbn,
                publicate_language=publicate_language)
        except Http404:
            book = Book.objects.create(title=title, author=authors, publicate_year=publicate_year,
                                       number_of_pages=number_of_pages, image=image, isbn_number=isbn,
                                       publicate_language=publicate_language)
    return redirect('books-all')


class BaseView(View):
    def get(self, request):
        return render(request, 'books/base_with_navbar.html')


class AllBooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('title')
        paginator = Paginator(books, 4)
        page_number = request.GET.get('page')
        page_queryset = paginator.get_page(page_number)
        return render(request, 'books/all_books.html', {'books': page_queryset})


class SearchBooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('title')
        paginator = Paginator(books, 4)
        page_number = request.GET.get('page')
        page_queryset = paginator.get_page(page_number)
        return render(request, 'books/search_books.html', {'books': page_queryset})

    def post(self, request):
        books = Book.objects.all().order_by('title')
        paginator = Paginator(books, 4)
        page_number = request.GET.get('page')
        page_queryset = paginator.get_page(page_number)
        title = request.POST.get('title')
        if title:
            page_queryset = books.filter(title__icontains=title)

        author = request.POST.get('author')
        if author:
            page_queryset = books.filter(author__icontains=author)

        year_from = request.POST.get('year_from')
        if year_from:
            page_queryset = books.filter(publicate_year__gte=year_from)

        year_to = request.POST.get('year_to')
        if year_to:
            page_queryset = books.filter(publicate_year__lte=year_to)

        language = request.POST.get('language')
        if language:
            page_queryset = books.filter(publicate_language__istartswith=language)
        return render(request, 'books/search_books.html', {'books': page_queryset, 'search_data': request.POST})


class AddBookView(View):
    def get(self, request):
        form = BookModelForm()
        return render(request, 'books/add_book_form.html', {'form': form})

    def post(self, request):
        form = BookModelForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('books-all')
        return render(request, 'books/add_book_form.html', {'form': form})


class DeleteBookView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        book.delete()
        return redirect('books-all')


class ModifyBookView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        form = BookModelForm(instance=book)
        return render(request, 'books/modify_form.html', {'form': form})

    def post(self, request, id):
        book = Book.objects.get(id=id)
        form = BookModelForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('books-all')
        return render(request, 'books/modify_form.html', {'form': form})


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
