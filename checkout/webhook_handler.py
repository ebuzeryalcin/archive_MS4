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