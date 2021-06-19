# Generating order number
import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
# Django countries package
from django_countries.fields import CountryField

from books.models import Book
from profiles.models import UserProfile


# Order model handling all orders, with fields used in an order
# Order number is unique and not editable
class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    # models.SET_NULL to keep order history even if profile is deleted
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    # To use django countries
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    # To prevent database lose an order if same order is placed twice
    original_bag = models.TextField(null=False, blank=False, default='')
    # Unique stripe pid created so orders dont get lost
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generating a random and unique order number using UUID of 32 characters
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        This method updates the total cost of bag every time a line item
        is added
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.delivery_cost = 2
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Overriding the original saving method and making sure a unique UUID
        exists for each order
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


# Specific item bag with its fields which is then added to total cost
class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    book = models.ForeignKey(Book, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Overriding save method, updating order total and to setup line
        item total.
        """
        self.lineitem_total = self.book.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'ISBN "{self.book.isbn}"" on order {self.order.order_number}'