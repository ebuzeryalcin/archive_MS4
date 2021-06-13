from django.urls import path
from . import views

# View for checkout page
urlpatterns = [
    path('', views.checkout, name='checkout')
]