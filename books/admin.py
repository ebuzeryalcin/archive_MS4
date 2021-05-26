from django.contrib import admin
from .models import Book, Category


# Fixing the order of books in admin
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'isbn',
        'name',
        'author',
        'category',
        'price',
        'image',
    )

    ordering = ('isbn',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


# Models for admin
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)