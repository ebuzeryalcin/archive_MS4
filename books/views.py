from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book

# Create your views here.


def all_books(request):
    """ This view is showing all books, its sorting and searching queries """

    # This returns all books from db
    books = Book.objects.all()

    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No search criteria is entered!")
                return redirect(reverse('books'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query) | Q(author__icontains=query)
            books = books.filter(queries)

    context = {
        'books': books,
        'search_term': query,
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