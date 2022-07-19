from django.urls import path
from rest_framework import routers
from . import views
from .views import UserAPIView

urlpatterns = [
    path('user', UserAPIView.as_view()),
    path('user/<str:pk>', UserAPIView.as_view()),  # to capture our ids
]