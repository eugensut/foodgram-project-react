from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet

from .views import UsersViewSet, TagViewSet, IngredientViewSet

app_name = "api"

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]