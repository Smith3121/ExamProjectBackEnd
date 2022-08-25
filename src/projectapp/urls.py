from rest_framework import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)

router.register('user', views.UserViewSet, basename='user')

router.register('treatment', views.TreatmentViewSet, basename='treatment')

router.register('reservation', views.ReservationViewSet, basename='reservation')

router.register('rating', views.RatingViewSet, basename='rating')

router.register('faq', views.FAQViewSet, basename='faq')

router.register('token', views.TokenViewSet, basename='user')

router.register('mtoken', views.MTokenViewSet, basename='user')

router.register('doctorlist', views.DoctorViewSet, basename='doctorlist')

router.register('docdescriptrem', views.RemoveDoctorDescriptionViewSet, basename='removedocdescr')

router.register('listuserres', views.ListUserReservationViewSet, basename='listuserres')

router.register('docresbyname', views.ListDoctorReservationByNameViewSet, basename='docresbyname')

router.register('doclistresbydate', views.ListDoctorReservationByDate, basename='doclistresbydate')

urlpatterns = router.urls
