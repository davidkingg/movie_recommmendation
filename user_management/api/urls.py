from django.urls import path
from . import views
from .views import UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('users', UserViewSet, basename='users_apiv')
urlpatterns = router.urls