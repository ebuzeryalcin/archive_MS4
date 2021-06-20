from django.urls import path
from . import views

# The root url
urlpatterns = [
    path('', views.all_books, name='books'),
    # To make django know the difference between integer and string
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    # String
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
]