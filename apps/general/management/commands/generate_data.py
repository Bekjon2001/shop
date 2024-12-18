import os
from django.db import transaction

from faker import Faker

from django.conf import settings
from django.utils.timezone import now
from django.core.management import BaseCommand
from faker.generator import random

from apps.abouts.models import About
from apps.categories.models import Category
from apps.general.service import random_image_download
from apps.general.models import General
from apps.products.models import Product

fake = Faker()


class Command(BaseCommand):
    @staticmethod
    def generate_about():
        today = now().date()
        if not About.objects.exists():

            django_filename = f'abouts/images/{today.year}/{today.month}/{today.day}/'
            image_dir = os.path.join(settings.MEDIA_ROOT, django_filename)
            image_name=random_image_download(image_dir)

            About.objects.create(
                title=fake.text(155),
                description=fake.text(255),
                image=os.path.join(django_filename, image_name),

            )
    @staticmethod
    def generate_products():
        today = now().date()
        django_filename = f'products/images/{today.year}/{today.month}/{today.day}/'
        image_dir = os.path.join(settings.MEDIA_ROOT, django_filename)
        image_name = random_image_download(image_dir)
        for cat_i in range(6):
            print(cat_i)
            category = Category.objects.create(
                name=fake.first_name(),
                category_images=os.path.join(django_filename, image_name),
            )
            if cat_i % 2:
                for i in range(3):
                    Category.objects.create(
                        name=fake.first_name(),
                        parent_id=category.pk
                    )


            products=[]
            for pro_i in range(10):
               products.append(
                   Product(
                       title=fake.text(50),
                       price=random.randint(5, 500),
                       old_price=random.randint(500, 1000),
                       currency=random.choice(General.Currency.choices)[0],
                       short_description=fake.text(255),
                       long_description=fake.text(10_000),
                       category_id=category.pk,
                       main_image=os.path.join(django_filename, image_name),

                   )
               )
            Product.objects.bulk_create(products)

    @transaction.atomic
    def handle(self, *args, **options):
        print(self.stdout.write(self.style.SUCCESS('Successfully generated about data')))
        self.generate_about()
        print(self.stdout.write(self.style.SUCCESS('Done')))

        # ====================== generate product model ======================
        print(self.stdout.write(self.style.SUCCESS('Successfully generated products data')))
        self.generate_products()
        print(self.stdout.write(self.style.SUCCESS('Done')))
