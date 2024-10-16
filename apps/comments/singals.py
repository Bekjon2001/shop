from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete

from apps.comments.models import ProductComment



@receiver((post_save, post_delete), sender=ProductComment)
def comment_post_save_or_post_delete(instance,*args, **kwargs):
    instance.product.comments_count = ProductComment.objects.filter(product_id=instance.product_id).count()
    instance.product.save()