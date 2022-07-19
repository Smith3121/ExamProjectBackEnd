from rest_framework import routers
from . import views
router = routers.DefaultRouter(trailing_slash=False)

router.register('user', views.UserViewSet, basename='user')
# router.register('token', views.TokenViewSet, basename='user')
# router.register('mtoken', views.MTokenViewSet, basename='user')

urlpatterns = router.urls
