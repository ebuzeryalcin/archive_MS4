from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
# Bag contents function,calculating current bag value,imported from contexts.py
from bag.contexts import bag_contents

# Installed stripe app
import stripe


# To get the bag from session
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty right now")
        return redirect(reverse('books'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51J2a5BCZzo3VPVgQDcaIYii4mKsqaD8qO4Rq6fcNiSBbwswHYWYgza4LvmCNTt1RsvvFuxxaOMqPmF8tgYhwuHTI005huViAdC',
        'client_secret': 'test_client_secret',
    }

    return render(request, template, context)