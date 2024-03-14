from django_filters.rest_framework import (
    FilterSet, ModelMultipleChoiceFilter, BooleanFilter
)
from django_filters import CharFilter
from django.db.models import Exists, OuterRef

from dishes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = []


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()
        return queryset.filter(
            Exists(user.favorites.filter(recipe=OuterRef('pk')))
        )

    def get_is_in_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()
        return queryset.filter(
            Exists(user.cart.filter(recipe=OuterRef('pk')))
        )

    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited']
