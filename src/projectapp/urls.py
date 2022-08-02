from django.urls import path
from rest_framework import routers
from . import views
from .views import UserAPIView, TreatmentAPIView, ReservationAPIView, DoctorAPIView, DateAPIView, RemoveDocDescrAPIView

urlpatterns = [
    path('api/user', UserAPIView.as_view()),
    path('api/user/<str:pk>', UserAPIView.as_view()),  # to capture our ids

    path('treatment', TreatmentAPIView.as_view()),
    path('treatment/<str:pk>', TreatmentAPIView.as_view()),  # to capture our ids

    path('api/reservation', ReservationAPIView.as_view()),
    path('api/reservation/<str:pk>', ReservationAPIView.as_view()),  # to capture our ids

    path('date', DateAPIView.as_view()),
    path('date/<str:pk>', DateAPIView.as_view()),  # to capture our ids

    path('hour', DateAPIView.as_view()),
    path('hour/<str:pk>', DateAPIView.as_view()),  # to capture our ids

    path('doctorlist', DoctorAPIView.as_view()),

    path('docdescrem/<str:pk>', RemoveDocDescrAPIView.as_view()),  # to capture our ids

]