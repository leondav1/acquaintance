from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_api_key.models import AbstractAPIKey


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CATEGORY_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='M', verbose_name='Пол')
    avatar = models.FileField(upload_to='files/avatar/', blank=True, null=True, verbose_name='Аватар')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


class UserAPIKey(AbstractAPIKey):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    @receiver(post_save, sender=User)
    def create_user_UserAPIKey(sender, instance, created, **kwargs):
        if created:
            UserAPIKey.objects.create_key(user=instance, name=instance.username)
