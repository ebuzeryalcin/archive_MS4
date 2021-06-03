from django.shortcuts import render

# Create your views here.

def view_bag(request):
    """ This view will render the bag page """

    return render(request, 'bag/bag.html')