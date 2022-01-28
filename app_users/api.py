from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from app_users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer, format=None):
        owner = self.request.user
        if self.request.data.get('avatar') is not None:
            avatar = self.request.data.get('avatar')
            serializer.save(owner=owner, avatar=avatar)
        else:
            serializer.save(owner=owner)
