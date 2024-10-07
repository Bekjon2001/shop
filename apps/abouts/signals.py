import os

from django.dispatch import receiver
from django.db.models.signals import post_delete

from apps.abouts.models import About



@receiver(post_delete, sender=About)
def delete_related_image(instance,**kwargs):
    os.remove(instance.image.path)