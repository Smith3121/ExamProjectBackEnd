from django.urls import path
from rest_framework import routers
from . import views
from .views import UserAPIView, TreatmentAPIView

urlpatterns = [
    path('user', UserAPIView.as_view()),
    path('user/<str:pk>', UserAPIView.as_view()),  # to capture our ids

    path('treatment', TreatmentAPIView.as_view()),
    path('treatment/<str:pk>', TreatmentAPIView.as_view()),  # to capture our ids
]