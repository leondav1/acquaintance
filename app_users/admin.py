from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin

from app_users.models import Profile, UserAPIKey


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender']


@admin.register(UserAPIKey)
class UserAPIKeyModelAdmin(APIKeyModelAdmin):
    list_display = ['name', 'prefix', 'created']
