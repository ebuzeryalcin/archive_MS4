from django.contrib import admin
from .models import Book, Category

# Models for admin
admin.site.register(Book)
admin.site.register(Category)