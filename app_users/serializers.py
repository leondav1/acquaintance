import os

from PIL import Image
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User

from acquaintance.settings import MEDIA_ROOT
from .models import Profile
from .utils import add_watermark


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['gender', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=make_password(validated_data.get('password')),
        )
        profile_data = validated_data.pop('profile')
        user.profile.gender = profile_data['gender']
        user.profile.avatar = profile_data['avatar']
        user.save()

        file_path_watermark = os.path.join(MEDIA_ROOT, "watermarks", "watermark.png")
        if profile_data['avatar'] and os.path.exists(file_path_watermark):
            img = Image.open(user.profile.avatar.path)
            watermark = Image.open(os.path.join(MEDIA_ROOT, "watermarks", "watermark.png"))
            result = add_watermark(img, watermark)
            result.save(user.profile.avatar.path)

        return user
