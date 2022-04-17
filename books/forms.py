from django import forms
from django.core.exceptions import ValidationError

from books.models import Book


def validate_isbn(value):
    value = value.strip()
    not_int = False
    try:
        int(value)
    except ValueError:
        not_int = True
    if not_int or len(value) != 10 and len(value) != 13:
        raise ValidationError(
            '"%(value)s" cannot be a proper ISBN number',
            params={'value': value},
        )


class BookForm(forms.Form):
    title = forms.CharField(max_length=256)
    author = forms.CharField(max_length=256)
    publicate_year = forms.IntegerField()
    number_of_pages = forms.IntegerField()
    isbn_number = forms.CharField(validators=[validate_isbn], label='ISBN')
    publicate_language = forms.CharField(max_length=64, label='Language')
    image = forms.ImageField(required=False, label='Cover')


class BookModifyForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class ImportBooksFromApiForm(forms.Form):
    title = forms.CharField(max_length=255, label='Title', required=False)
    author = forms.CharField(max_length=128, label='Author', required=False)
    publisher = forms.CharField(max_length=128, label='Publisher', required=False)
    subject = forms.CharField(max_length=64, label='Subject', required=False)
    isbn = forms.CharField(min_length=10, max_length=13, label='ISBN', required=False)
    lccn = forms.CharField(max_length=128, label='Library of Congress Control Number', required=False)
    oclc = forms.CharField(max_length=128, label='Online Computer Library Center number', required=False)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        publisher = cleaned_data.get('publisher')
        subject = cleaned_data.get('subject')
        isbn = cleaned_data.get('isbn')
        lccn = cleaned_data.get('lccn')
        oclc = cleaned_data.get('oclc')
        if not (title or author or publisher or subject or isbn or lccn or oclc):
            raise forms.ValidationError('At least one field must be filled')
