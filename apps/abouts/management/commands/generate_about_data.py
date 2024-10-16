import os
from django.db import transaction

from faker import Faker

from django.conf import settings
from django.utils.timezone import now
from django.core.management import BaseCommand

from apps.abouts.models import About
from apps.general.service import  random_image_download


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

    @transaction.atomic
    def handle(self, *args, **options):
        # ====================== generate about model ======================
        print(self.stdout.write(self.style.SUCCESS('Successfully generated about data')))
        self.generate_about()