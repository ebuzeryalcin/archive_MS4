from django.shortcuts import render, get_object_or_404

# For profile page
from .models import UserProfile

def profile(request):
    """ To display the user's profile. """
    # Returning to template
    profile = get_object_or_404(UserProfile, user=request.user)

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
    }

    return render(request, template, context)