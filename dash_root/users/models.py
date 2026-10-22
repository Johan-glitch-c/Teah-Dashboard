from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    img = models.ImageField(upload_to = "avatars/", default= 'default.jpg')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
