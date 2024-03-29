from django.db import models


class Category(models.Model):
    # Fixing spelling in admin
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    # If there is a friendly name
    def get_friendly_name(self):
        return self.friendly_name


class Book(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    isbn = models.CharField(max_length=15)
    name = models.CharField(max_length=254)
    description = models.TextField()
    author = models.CharField(max_length=254, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
