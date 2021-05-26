from django.urls import path
from . import views

# The root url
urlpatterns = [
    path('', views.all_books, name='books')
]