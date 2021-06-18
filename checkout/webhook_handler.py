from django.http import HttpResponse


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

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
        save_info = intent.metadata.saveinfo

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # If there is no string in some shipping details its replaced with none
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # If order does not exist
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
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already exists in database',
                    status=200)

            return HttpResponse(
                content=f'Webhook received: {event["type"]}',
                status=200)

        # If and when a payment has failed
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)