from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from books.models import Book

# Create your views here.


# Rendering bag page
def view_bag(request):
    """ This view will render the bag page """

    return render(request, 'bag/bag.html')


# Adding book to bag
def add_to_bag(request, book_id):
    """ Adding quantity of the book to the shopping bag """

    book = get_object_or_404(Book, pk=book_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    # If same book is added
    if book_id in list(bag.keys()):
        bag[book_id] += quantity
        messages.success(
            request, f'{book.name} quantity updated to {bag[book_id]}')
    # If book is added
    else:
        bag[book_id] = quantity
        messages.success(request, f'Added {book.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, book_id):
    """ Adjust the quantity of the specified book to the specified amount """

    book = get_object_or_404(Book, pk=book_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    # When bag is updated
    if quantity > 0:
        bag[book_id] = quantity
        messages.success(
            request, f'{book.name} quantity updated to {bag[book_id]}')
    else:
        bag.pop(book_id)
        messages.success(request, f'Removed {book.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, book_id):
    """ Removing book from bag """

    try:
        book = get_object_or_404(Book, pk=book_id)
        bag = request.session.get('bag', {})

        bag.pop(book_id)
        messages.success(request, f'Removed {book.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    # If there is an error while removing
    except Exception as e:
        messages.error(request, f'Error while removing book: {e}')
        return HttpResponse(status=500)