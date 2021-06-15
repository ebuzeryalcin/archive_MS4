from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


# To get the bag from session
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty right now")
        return redirect(reverse('books'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51J2a5BCZzo3VPVgQDcaIYii4mKsqaD8qO4Rq6fcNiSBbwswHYWYgza4LvmCNTt1RsvvFuxxaOMqPmF8tgYhwuHTI005huViAdC',
        'client_secret': 'test_client_secret',
    }

    return render(request, template, context)