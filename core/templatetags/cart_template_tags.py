from django import template
from core.models import Order
register = template.Library()



@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def get_country(country_code):
    country = ''
    if country_code == 'en':
        country = 'united-kingdom'
    elif country_code == 'tk':
        country = 'turkmenistan'
    else:
        country = 'russia'
    return country

@register.filter
def multiply(a):
    b = a*3.5
    return b