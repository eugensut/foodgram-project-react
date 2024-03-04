from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (
    GetFollowViewSet, DeletePostFollowViewSet, UsersViewSet,
    TagViewSet, IngredientViewSet, RecipeViewSet, FavoriteViewSet,
    GetCartViewSet, PostCartViewSet
)

app_name = "api"

router = DefaultRouter()

"""router.register(
    r'users/subscriptions', GetFollowViewSet, basename='subscriptions'
)"""
router.register(r'users', UsersViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(
    r'ingredients', IngredientViewSet, basename='ingredients'
)
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorites'
)

urlpatterns = [
    path('recipes/<int:recipe_id>/shopping_cart/', PostCartViewSet.as_view()),
    path(
        'recipes/download_shopping_cart/',
        GetCartViewSet.as_view({'get': 'list'})
    ),
    path('users/subscriptions/', GetFollowViewSet.as_view({'get': 'list'})),
    path(
        'users/<int:author_id>/subscribe/', DeletePostFollowViewSet.as_view()
    ),
    path('', include(router.urls)),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
