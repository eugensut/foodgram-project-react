from django.contrib import admin

from .models import Tag, Ingredient

DEFAULT_EMPTY_VALUE = '-empty-'


class TagAdmin(admin.ModelAdmin):
    empty_value_display = DEFAULT_EMPTY_VALUE


class IngredientAdmin(admin.ModelAdmin):
    empty_value_display = DEFAULT_EMPTY_VALUE


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
