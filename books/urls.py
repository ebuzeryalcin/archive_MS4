from django.urls import path
from . import views

# The root url
urlpatterns = [
    path('', views.all_books, name='books'),
    # To make django know the difference between integer and string
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    # String
    path('add/', views.add_book, name='add_book'),
]