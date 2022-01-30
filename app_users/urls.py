from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from app_users.api import UserCreateAPIView, apikey


urlpatterns = [
    path('clients/create/', UserCreateAPIView.as_view()),
    path('apikey', apikey),
]

urlpatterns = format_suffix_patterns(urlpatterns)
