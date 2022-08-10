from django.urls import path
from rest_framework import routers
from . import views
from .views import UserViewSet, TreatmentViewSet, ReservationViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register('user', views.UserViewSet, basename='user')
router.register('user/<str:pk>', views.UserViewSet, basename='user')

router.register('treatment', views.TreatmentViewSet, basename='treatment')
router.register('treatment/<str:pk>', views.TreatmentViewSet, basename='treatment')

router.register('reservation', views.ReservationViewSet, basename='reservation')
router.register('reservation/<str:pk>', views.ReservationViewSet, basename='reservation')

router.register('token', views.TokenViewSet, basename='user')

router.register('mtoken', views.MTokenViewSet, basename='user')

router.register('doctorlist', views.DoctorViewSet, basename='doctorlist')

router.register('docdescriptrem/<str:pk>', views.RemoveDoctorDescriptionViewSet, basename='removedocdescr')

router.register('listuserres/<str:pk>', views.ListUserReservationViewSet, basename='listuserres')

router.register('docresbyname/<str:pk>', views.ListDoctorReservationByNameViewSet, basename='docresbyname')

router.register('doclistresbydate/<str:pk>', views.ListDoctorReservationByDate, basename='doclistresbydate')

urlpatterns = router.urls
