from django.shortcuts import render, get_object_or_404
from django.contrib import messages

# For profile page
from .models import UserProfile

from .forms import UserProfileForm


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