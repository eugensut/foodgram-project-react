from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet

from .views import UsersViewSet

app_name = "api"

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]