import requests
from django.core.exceptions import ValidationError
from django.db import models
from django.core.cache import cache
from django.utils.timezone import now
from .validation_phone import check_uzb_number


class General(models.Model):
    class Currency(models.TextChoices):
        USD = 'USD', 'USD'
        RUB = 'RUB', 'RUB'
        UZS = 'UZS', 'UZS'
        EUR = 'EUR', 'EUR'
        JPY = 'JPY', 'JPY'



    DEFAULT_CURRENCY = Currency.UZS


    phone1 = models.CharField(max_length=13, validators=[check_uzb_number], help_text="UZB Number +998123456789")
    phone2 = models.CharField(max_length=13, null=True, blank=True, validators=[check_uzb_number])
    location = models.URLField()
    address = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to="general/logo/image/%Y/%m/%d/")

    def clean(self):
        if self.pk and General.objects.exists():
            raise ValidationError('Unique')


class GeneralSocialMedia(models.Model):
    url = models.URLField()
    icon = models.ImageField(upload_to="social_links/icon/image/%Y/%m/%d/")


class CurrencyAmount(models.Model):
    GET_CURRENCY_URL = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/{currency}/{date}/ '
    currency = models.CharField(max_length=10, choices=General.Currency.choices)
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    @classmethod
    def get_currency_amount(cls, currency: str):
        today = now().date()

        amount_in_uzs = cache.get(currency)

        if not amount_in_uzs:

            response = requests.get(cls.GET_CURRENCY_URL.format(currency=currency, date=today))

            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    usd_amount = data[0]['Rate']
                else:
                    usd_amount = 0
            else:
                usd_amount = 0

            obj,created = cls.objects.get_or_create(
                currency=currency,
                date=today,
                defaults={
                    'usd_amount': usd_amount
                }

            )
            cache.set(currency,obj.usd_amount)
            amount_in_uzs=cache.get(currency)


        return amount_in_uzs


    class Meta:
        unique_together = (('currency', 'date'),)

