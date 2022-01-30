from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.models import APIKey

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


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def apikey(request):
    username = request.user.username
    if request.method == 'GET':
        response = {}
        keys = APIKey.objects.all()
        for key in keys:
            if key.name == username:
                response['apikey'] = key.prefix + '*****'
                response['created'] = key.created
                response['expires'] = key.expiry_date
                break
        return Response(response, status=status.HTTP_200_OK)
    else:
        keys = APIKey.objects.all()
        for key in keys:
            if key.name == username:
                key.delete()
                break
        api_key, key = APIKey.objects.create_key(name=request.user.username)
        expires = datetime.now() + timedelta(days=90)
        expires = make_aware(expires)
        api_key.expiry_date = expires
        api_key.save()
        return Response({'apikey': key, 'expires': expires}, status=status.HTTP_200_OK)
