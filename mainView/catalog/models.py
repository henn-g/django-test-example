import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="name of genre")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='enter author summary')
    isbn = models.CharField('ISBN', max_length=13)

    genre = models.ManyToManyField(Genre, help_text='select genre for this book')

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    book = models.ForeignKey('Book', on_delete = models.SET_NULL, null=True)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null = True, blank = True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )
    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text = 'Book availability',
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    firstName = models.CharField(max_length = 100)
    lastName = models.CharField(max_length = 100)
    dateOfBirth = models.DateField(null = True, blank = True)
    dateOfDeath = models.DateField('Died', null = True, blank = True)

    class Meta:
        ordering = ['lastName', 'firstName']

    def __str__(self):
        return f'{self.lastName}, {self.firstName}'
