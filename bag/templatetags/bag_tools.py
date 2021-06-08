from django import template


# Custom template filter to calculate subtotal in bag page
register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity