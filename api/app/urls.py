from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as auth_views

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'holidays', views.HolidayViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', auth_views.obtain_auth_token)
]
