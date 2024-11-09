from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=120)
    message = models.TextField(max_length=5000)
    subject= models.CharField(max_length=200)