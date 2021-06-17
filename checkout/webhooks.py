# For stripe api secrets
from django.conf import settings
# For exception handler
from django.http import HttpResponse
# Post request decodator
from django.views.decorators.http import require_POST
# Stripe will not send csrf token
from django.views.decorators.csrf import csrf_exempt
# Webhook handler class
from checkout.webhook_handler import StripeWH_Handler

import stripe

# Stripe docs, https://stripe.com/docs/webhooks

@require_POST
@csrf_exempt
def webhook(request):
    """Listening to webhooks comming from stripe"""
    # Setup webhook secret and stripe api key
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
        # Catching exceptions other than what stripe has given
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

    print('success!!!!!!')
    # Call the event handler with the event
    response = event_handler(event)
    return response