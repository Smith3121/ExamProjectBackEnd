from django.urls import path
from rest_framework import routers
from . import views
from .views import UserViewSet, TreatmentViewSet, ReservationViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register('user', views.UserViewSet, basename='user')
router.register('user/<str:pk>', views.UserViewSet, basename='user')
router.register('token', views.TokenViewSet, basename='user')
router.register('mtoken', views.MTokenViewSet, basename='user')
router.register('treatment', views.TreatmentViewSet, basename='treatment')
router.register('treatment/<str:pk>', views.TreatmentViewSet, basename='treatment')
router.register('reservation', views.ReservationViewSet, basename='reservation')
router.register('reservation/<str:pk>', views.ReservationViewSet, basename='reservation')
router.register('date', views.DateViewSet, basename='date')
router.register('date/<str:pk>', views.DateViewSet, basename='date')
router.register('doctorlist', views.DoctorViewSet, basename='doctorlist')
router.register('docdescriptrem/<str:pk>', views.RemoveDocDescrViewSet, basename='removedocdescr')
router.register('listuserres/<str:pk>', views.ListUserResViewSet, basename='listuserres')
router.register('docpatres/<str:pk>', views.DocPatResViewSet, basename='docpatres')
router.register('doclistresbydate/<str:pk>', views.DocListResByDateViewSet, basename='doclistresbydate')

urlpatterns = router.urls
