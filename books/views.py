from django.shortcuts import render
from .models import Book

# Create your views here.


def all_books(request):
    """ This view is showing all books, its sorting and searching queries """

    # This returns all books from db
    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, 'books/books.html', context)