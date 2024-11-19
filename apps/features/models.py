from django.db import models

class Feature(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        to='categories.Category',
        on_delete=models.PROTECT,
        limit_choices_to={
            'parent__isnull':False
        }
    )

    def clean(self):
            if not self.category.parent:
                raise ValueError({'category not parent'})

    def __str__(self):
        return self.name


class FeatureValue(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.PROTECT,related_name='values')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = (('feature', 'name'),)

    def __str__(self):
        return self.name + '' + self.feature.name