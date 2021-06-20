from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book, Category

# Book add view
from .forms import BookForm


def all_books(request):
    """ This view is showing all books, its sorting and searching queries """

    # This returns all books from db
    books = Book.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        # Requesting sort, searching for a name if there is
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                books = books.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            # order by model
            books = books.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            books = books.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # If failing entering search criteria
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No search criteria is entered!")
                return redirect(reverse('books'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query) | Q(author__icontains=query)
            books = books.filter(queries)

    # returning sorting methodology to template
    current_sorting = f'{sort}_{direction}'

    context = {
        'books': books,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
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


def add_book(request):
    """ Add a book to store """
    if request.method == 'POST':
        # FILES to successfully add image if there is
        form = BookForm(request.POST, request.FILES)
        # If successful
        if form.is_valid():
            # Storing saved book
            book = form.save()
            messages.success(request, 'Successfully added book!')
            return redirect(reverse('book_detail', args=[book.id]))
        # If failed
        else:
            messages.error(request, 'Failed to add book. Please ensure the form is valid.')
    else:
        form = BookForm()

    template = 'books/add_book.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_book(request, book_id):
    """ Edit a book in the store """
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        # Telling to update specifically chosen book with instance
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated book!')
            return redirect(reverse('book_detail', args=[book.id]))
        else:
            messages.error(request, 'Failed to update book. Please ensure the form is valid.')
    else:
        form = BookForm(instance=book)
        messages.info(request, f'You are editing {book.name}')

    template = 'books/edit_book.html'
    context = {
        'form': form,
        'book': book,
    }

    return render(request, template, context)


def delete_book(request, book_id):
    """ Delete a book from the store, POST not required """
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, 'Book deleted!')
    return redirect(reverse('books'))