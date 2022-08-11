from django.urls import path
from rest_framework import routers
from . import views
from .views import UserViewSet, ReservationViewSet, TreatmentAPIView

router = routers.SimpleRouter(trailing_slash=False)

router.register('user', views.UserViewSet, basename='user')

# router.register('treatment', TreatmentAPIView.as_view(), basename='treatment')

router.register('reservation', views.ReservationViewSet, basename='reservation')

router.register('token', views.TokenViewSet, basename='user')

router.register('mtoken', views.MTokenViewSet, basename='user')

router.register('doctorlist', views.DoctorViewSet, basename='doctorlist')

router.register('docdescriptrem', views.RemoveDoctorDescriptionViewSet, basename='removedocdescr')

router.register('listuserres', views.ListUserReservationViewSet, basename='listuserres')

router.register('docresbyname', views.ListDoctorReservationByNameViewSet, basename='docresbyname')

router.register('doclistresbydate', views.ListDoctorReservationByDate, basename='doclistresbydate')

urlpatterns = router.urls
