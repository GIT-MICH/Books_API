from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    publicate_year = models.IntegerField(null=True)
    number_of_pages = models.IntegerField(null=True)
    isbn_number = models.IntegerField()
    publicate_language = models.CharField(max_length=64)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

    def delete_book_url(self):
        return reverse('book-delete', args=(self.id,))

    def modify_book_url(self):
        return reverse('book-modify', args=(self.id,))
