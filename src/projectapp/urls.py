from django.urls import path
from rest_framework import routers
from . import views
from .views import UserAPIView, TreatmentAPIView, ReservationAPIView, DoctorAPIView, DateAPIView, RemoveDocDescrAPIView, \
    ListUserResAPIView, DocPatResAPIView, DocListResByDateAPIView

urlpatterns = [
    path('api/user', UserAPIView.as_view()),
    path('api/user/<str:pk>', UserAPIView.as_view()),  # to capture our ids

    path('api/treatment', TreatmentAPIView.as_view()),
    path('api/treatment/<str:pk>', TreatmentAPIView.as_view()),  # to capture our ids

    path('api/reservation', ReservationAPIView.as_view()),
    path('api/reservation/<str:pk>', ReservationAPIView.as_view()),  # to capture our ids

    path('date', DateAPIView.as_view()),
    path('date/<str:pk>', DateAPIView.as_view()),  # to capture our ids

    path('api/doctorlist', DoctorAPIView.as_view()),

    path('docdescrem/<str:pk>', RemoveDocDescrAPIView.as_view()),  # to capture our ids

    path('listuserres/<str:pk>', ListUserResAPIView.as_view()),  # to capture our ids

    path('docpatres/<str:pk>', DocPatResAPIView.as_view()),  # to capture our ids

    path('doclistresbydate/<str:pk>', DocListResByDateAPIView.as_view()),  # to capture our ids


]