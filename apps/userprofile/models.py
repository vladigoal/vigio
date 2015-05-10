from django.db import models
from django.contrib.auth.models import User


class ShopUser(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=128, verbose_name='Phone')