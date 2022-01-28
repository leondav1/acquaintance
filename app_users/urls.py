from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from app_users.api import UserCreateAPIView


urlpatterns = [
    path('clients/create/', UserCreateAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
