import requests
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from books.forms import BookForm, BookModifyForm, ImportBooksFromApiForm
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
        publishedDate = book.get('publishedDate')
        publicate_year = int(publishedDate[:4])
        isbns = book.get('industryIdentifiers', [])
        isbn = None
        for isbn in isbns:
            if isbn['type'] == 'ISBN_10':
                isbn = isbn['identifier']
            elif isbn['type'] == 'ISBN_13':
                isbn = isbn['identifier']
        number_of_pages = book.get('pageCount')
        publicate_language = book.get('language')
        image = book.get('imageLinks')
        if image:
            image = image.get('thumbnail')
        try:
            book = get_object_or_404(
                Book, title=title, author=authors, publicate_year=publicate_year,
                number_of_pages=number_of_pages, isbn_number=isbn,
                publicate_language=publicate_language, image=image)
        except Http404:
            book = Book.objects.create(title=title, author=authors, publicate_year=publicate_year,
                                       number_of_pages=number_of_pages, isbn_number=isbn,
                                       publicate_language=publicate_language, image=image)
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
        form = BookForm()
        return render(request, 'books/add_book_form.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            publicate_year = form.cleaned_data.get('publicate_year')
            number_of_pages = form.cleaned_data.get('number_of_pages')
            isbn_number = form.cleaned_data.get('isbn_number')
            publicate_language = form.cleaned_data.get('publicate_language')
            image = form.cleaned_data.get('image')
            Book.objects.create(**form.cleaned_data)
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
        form = BookModifyForm(instance=book)
        return render(request, 'books/modify_form.html', {'form': form})

    def post(self, request, id):
        book = Book.objects.get(id=id)
        form = BookModifyForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('books-all')
        return render(request, 'books/modify_form.html', {'form': form})


class ImportBooksFromApiView(View):
    def get(self, request):
        form = ImportBooksFromApiForm()
        return render(request, 'books/import_form.html', {'form': form})

    def post(self, request):
        url = 'https://www.googleapis.com/books/v1/volumes?q='
        form = ImportBooksFromApiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            publisher = form.cleaned_data.get('publisher')
            subject = form.cleaned_data.get('subject')
            isbn = form.cleaned_data.get('isbn')
            lccn = form.cleaned_data.get('lccn')
            oclc = form.cleaned_data.get('oclc')
            if title:
                url += f'+intitle:{title}'
            if author:
                url += f'+inauthor:{author}'
            if publisher:
                url += f'+inpublisher:{publisher}'
            if subject:
                url += f'+subject:{subject}'
            if isbn:
                url += f'+isbn:{isbn}'
            if lccn:
                url += f'+lccn:{lccn}'
            if oclc:
                url += f'+intitle:{oclc}'
            get_books_from_googleapi(request, url=url)
            return redirect('books-all')
        return render(request, 'books/import_form.html', {'form': form})


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
