from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
    to='self',
    null=True,
    blank=True,
    related_name='children',
    on_delete=models.CASCADE,
    related_query_name='category'
     )
    category_images=models.ImageField(upload_to='categories/images/%Y/%m/%d/')

    def clean(self):
        try:
            if not self.pk and self.parent.parent:
                raise ValidationError('you can creat only three category')
        except AttributeError:
            pass


    def category_filter(self):
        if self.parent is None:
            return self.name
        elif self.children.exists():
            return self.name
        elif self.parent.parent is not None and not self.children.exists():
            return self.name
        return None

    def is_leaf(self):
        # Checks if the category is a leaf node (no children)
        return self.children.count() == 0

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']