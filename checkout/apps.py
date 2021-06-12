from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    # Overriding original method to import signals module
    def ready(self):
        import checkout.signals
