from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CATEGORY_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='M', verbose_name='Пол')
    avatar = models.FileField(upload_to='files/avatar/', blank=True, null=True, verbose_name='Аватар')
