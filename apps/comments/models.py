from django.contrib.auth.models import User
from django.db import models
from django.forms import CharField, EmailField
from django.core.validators import MinValueValidator, MaxValueValidator




class ProductComment(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    message = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if self.user:
            self.name, self.email = self.user.get_full_nema(), self.email

        super().save(*args,**kwargs)

