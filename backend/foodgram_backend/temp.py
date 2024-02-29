ingredients = validated_data.pop('ingredients')
    for idx, value in enumerate(ingredients):
        recipe_ingredients[idx].objects.update_or_create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=value['id']),
                amount=value['amount']
        )
        recipe_ingredients = [IngredientInRecipe] * len(ingredients)