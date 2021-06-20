from django.shortcuts import render, get_object_or_404
from django.contrib import messages

# For profile page
from .models import UserProfile

from .forms import UserProfileForm
# Order history view, from order model
from checkout.models import Order


def profile(request):
    """ To display the user's profile. """
    # Returning to template
    profile = get_object_or_404(UserProfile, user=request.user)

    # Post handler for profile view, when user update profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        # Rendering to profile page
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    # reusing checkout_success template
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        # Checking if order is from order history view
        'from_profile': True,
    }

    return render(request, template, context)