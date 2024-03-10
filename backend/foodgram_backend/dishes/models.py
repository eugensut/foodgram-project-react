from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from colorfield.fields import ColorField

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(
        'Picture',
        upload_to='dishes/',
        blank=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(3600), MinValueValidator(1)]
    )

    tags = models.ManyToManyField(
        Tag, related_name='recipes'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientInRecipe'
    )

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_recipes'
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(9999), MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'favorites'
        verbose_name = 'Favorite'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe'
            )
        ]

    def __str__(self):
        return f'Favorite recipe {self.recipe} for user {self.user}.'


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'cart'
        verbose_name = 'Shopping cart'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recip_in_cart'
            )
        ]

    def __str__(self):
        return (f'The user {self.user} bought this recipe {self.recipe}')
