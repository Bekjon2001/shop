from decimal import Decimal
from email.policy import default

from django.core.validators import MinValueValidator
from django.db import models

from apps.categories.models import Category
from apps.comments.models import ProductComment
from apps.general.models import General
from apps.ratings.models import ProductRating


class Product(models.Model):
    title = models.CharField(max_length=155)
    avg_rating = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        default=Decimal('0'),
        editable=False
    )
    comments_count = models.DecimalField(
        max_digits=20,
        decimal_places=0,
        default=Decimal('0'),
        editable=False,
    )
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        editable=False,
        default=0
    )
    old_price = models.DecimalField(max_digits=8, decimal_places=2, editable=False,default=0 )
    currency = models.CharField(
        choices=General.Currency.choices,
        default=General.DEFAULT_CURRENCY,
        max_length=5
    )
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(max_length=10_000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    added_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to='products/images/%Y/%m/%d/')

    def set_avg_rating(self):
        aggregated_amount = ProductRating.objects.filter(
            product_id=self.pk
        ).aggregate(
            avg=models.Avg('rating', default=0),
        )
        self.avg_rating = round(aggregated_amount['avg'], 1)
        self.save()

    def set_comments_rating(self):
        self.comments_count = ProductComment.objects.filter(product_id=self.pk).count()
        self.save()



    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/')
    ordering_number = models.PositiveSmallIntegerField(default=0)


class ProductFeatures(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature_value = models.ManyToManyField('features.FeatureValue', )
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Enter in UZS'
    )
    old_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Enter in UZS'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.product.price, self.product.iod_price, = self.price, self.old_price
        self.product.save()
