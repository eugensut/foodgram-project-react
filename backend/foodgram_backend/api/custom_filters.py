from django_filters.rest_framework import FilterSet
from django_filters import CharFilter

from dishes.models import Ingredient


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = []
