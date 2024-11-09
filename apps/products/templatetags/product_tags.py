from decimal import Decimal

from django import template

from apps.general.models import CurrencyAmount, General
from apps.wishlist.models import Wishlist

register = template.Library()


@register.simple_tag
def decimal_to_range(decimal_number):
    return range(int(decimal_number))

@register.simple_tag
def product_in_wishlist(user_id: int, product_id: int)-> bool:
    return Wishlist.objects.filter(user_id=user_id, product_id=product_id).exists()

@register.simple_tag
def get_price_currency(to_currency:str, price: Decimal = 0)-> Decimal:
    if to_currency == General.Currency.UZS:
        return price

    return round(price /Decimal( CurrencyAmount.get_currency_amount(currency=to_currency)),2)




@register.simple_tag
def multiply(value1, value2):
    print(type(value1),type(value2))
    return round((value1 / 100) * value2, 2)


@register.simple_tag
def add(value1,value2):
    return Decimal(value1) + value2