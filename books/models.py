from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.ManyToManyField('Author')
    publicate_date = models.DateField(null=True)
    pages = models.IntegerField(null=True)
    image = models.ImageField(blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, null=True)
    isbn_10 = models.CharField(max_length=10, null=True)
    publicate_language = models.ForeignKey('Language', on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.CharField(max_length=124)

    def __str__(self):
        return self.language
