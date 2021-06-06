from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages

from books.models import Book

# Create your views here.

def view_bag(request):
    """ This view will render the bag page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, book_id):
    """ Adding quantity of the book to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if book_id in list(bag.keys()):
        bag[book_id] += quantity
    else:
        bag[book_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, book_id):
    """ Adjust the quantity of the specified book to the specified amount """

    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[book_id] = quantity
    else:
        bag.pop(book_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))