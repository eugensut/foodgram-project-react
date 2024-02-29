from django.contrib import admin

from .models import Tag, Ingredient, Recipe, IngredientInRecipe

DEFAULT_EMPTY_VALUE = '-empty-'


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 3
    verbose_name = "ingredient"


class TagAdmin(admin.ModelAdmin):
    empty_value_display = DEFAULT_EMPTY_VALUE


class IngredientAdmin(admin.ModelAdmin):
    empty_value_display = DEFAULT_EMPTY_VALUE


class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = DEFAULT_EMPTY_VALUE
    list_display = (
        'pk',
        'name',
        'cooking_time',
        'author'
    )
    filter_horizontal = ('tags',)
    inlines = (RecipeIngredientInline,)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
