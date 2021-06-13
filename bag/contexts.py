from django.shortcuts import get_object_or_404
from books.models import Book


def bag_contents(request):

    bag_items = []
    total = 0
    book_count = 0
    delivery = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        book = get_object_or_404(Book, pk=item_id)
        total += quantity * book.price
        if total >= 1:
            delivery = 2
        # if there is no books in bag delivery shows 0
        else:
            delivery = 0
        book_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'book': book,
            'delivery': delivery,
        })

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'book_count': book_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context