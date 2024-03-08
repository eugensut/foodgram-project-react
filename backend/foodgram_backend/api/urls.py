from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (
    UsersViewSet, TagViewSet, IngredientViewSet,
    RecipeViewSet, GetCartViewSet, PostCartViewSet
)

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(
    r'ingredients', IngredientViewSet, basename='ingredients'
)
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('recipes/<int:recipe_id>/shopping_cart/', PostCartViewSet.as_view()),
    path(
        'recipes/download_shopping_cart/',
        GetCartViewSet.as_view({'get': 'list'})
    ),
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
