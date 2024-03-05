from django_filters.rest_framework import (
    FilterSet, ModelMultipleChoiceFilter, BooleanFilter
)
from django_filters import CharFilter
from django.db.models import Exists, OuterRef
from dishes.models import Ingredient, Recipe, Tag, Favorite


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='startswith')

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

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()
        return queryset.filter(
            Exists(user.favorites.filter(recipe=OuterRef('pk')))
        )
           
    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited']
