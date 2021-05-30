from django.shortcuts import render, get_object_or_404
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


def book_detail(request, book_id):
    """ This view is showing book details when clicking on one """

    # This gets the book id from the db
    book = get_object_or_404(Book, pk=book_id)

    context = {
        'book': book,
    }

    return render(request, 'books/book_detail.html', context)