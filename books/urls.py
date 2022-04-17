from django.urls import path
from books.views import (AllBooksView,
                         BookListView,
                         AddBookView,
                         DeleteBookView,
                         ModifyBookView,
                         SearchBooksView,
                         ImportBooksFromApiView,
                         )

urlpatterns = [
    path('all/', AllBooksView.as_view(), name='books-all'),
    path('add/', AddBookView.as_view(), name='book-add'),
    path('delete/<int:id>/', DeleteBookView.as_view(), name='book-delete'),
    path('modify/<int:id>/', ModifyBookView.as_view(), name='book-modify'),
    path('search/', SearchBooksView.as_view(), name='books-search'),
    path('import/', ImportBooksFromApiView.as_view(), name='books-import'),
    path('book/<int:pk>/', BookListView.as_view(), name='book-api'),

]
