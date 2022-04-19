Application to manage book collection.

Project idea: The purpose of the created application is manage collection of books. Books might be added, modified or delete and also imported from API Google.

** APP SUMMARY **

MODELS: 1.

Books

FORMS: 3.

BookForm
BookModifyForm
ImportBooksFromApiForm


VIEWS: 7.

    'all/', AllBooksView;
    'add/', AddBookView;
    'delete/<int:id>/', DeleteBookView;
    'modify/<int:id>/', ModifyBookView;
    'search/', SearchBooksView;
    'import/', ImportBooksFromApiView;
    'book_api/', BookListView;

TESTS: 11.
