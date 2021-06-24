from django.http import HttpResponse
# Email imports to send email confirmation
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from books.models import Book
# For anonymous/user as below in code
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    # Method to send confirmation email
    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        # Rendering customer email
        cust_email = order.email
        # Rendering email files to strings
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

        # Taking the event stripe is sending and returning
        # an http response that event was recieved
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        # Recieving event
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

        # Sending each time payment is succeeded
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        # Getting from the metadata added in checkout/views.py
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # If there is no string in some shipping details its replaced with none
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # When save_info is checked update profile info with webhook
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()

        # If order does not exist, attempting to find order
        order_exists = False
        attempt = 1
        while attempt <= 5:
            # Trying to get the order from pid with iexact match to find
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # If order exists
                order_exists = True
                # If order is found breaking the attempting time loop
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            # Sending email to customer, if email is found in db
            self._send_confirmation_email(order)
            # Sending message to stripe order already exists
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | \
                        SUCCESS: Verified order already exists in database',
                    status=200)
        else:
            # When order doesnt exist after several attempts, will be created
            # as same as when a form is submitted
            order = None
            try:
                # No form, instead creating an order like above
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # From views.py, loading from json instead of session
                for item_id, item_data in json.loads(bag).items():
                    book = Book.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            book=book,
                            quantity=item_data,
                        )
                        order_line_item.save()
            except Exception as e:
                # If anything goes wrong, delete order, send message to stripe
                if order:
                    order.delete()
                return HttpResponse(
                    # Stripe will try webhook later again
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        # If order is created by webhook handler, send by here, before
        # returning to stripe
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                SUCCESS: Created order in webhook',
            status=200)

        # If and when a payment has failed
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)