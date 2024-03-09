import base64

from rest_framework import serializers
from rest_framework.validators import ValidationError, UniqueTogetherValidator
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.utils import timezone

from users.models import User, Follow
from dishes.models import (
    Tag, Ingredient, IngredientInRecipe, Recipe, Favorite, Cart
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class UserReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        )


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password'

        )
        lookup_field = 'username'
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'username': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientInRecipetReadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    id = serializers.IntegerField(source='ingredient.id')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(required=False, many=True)
    author = UserReadSerializer()
    ingredients = IngredientInRecipetReadSerializer(
        source='amount_recipes', many=True, read_only=True
    )
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'text',
            'cooking_time',
            'image',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    pub_date = serializers.HiddenField(default=timezone.now)
    author = UserReadSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientInRecipetReadSerializer(
        source='amount_recipes', many=True, read_only=True
    )
    is_favorited = serializers.BooleanField(default=False, read_only=True)
    is_in_shopping_cart = serializers.BooleanField(
        default=False, read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'pub_date',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagSerializer(instance.tags, many=True).data
        return data

    def validate_cooking_time(self, value):
        if value < 1:
            raise ValidationError('the value must be greater than 0')
        return value

    def validate_tags(self, value):
        if len(value) != len(set(value)):
            raise ValidationError('is duplicated.')
        return value

    def validate_empty_values(self, data):
        if not data.get('tags'):
            raise ValidationError(
                {'tags': 'This field is required.'}
            )
        ingredients = data.get('ingredients')
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'This field is required.'}
            )
        unique = set()
        for dct in ingredients:
            pk = dct.get('id')
            if pk in unique:
                raise ValidationError(
                    {f'id {pk}': 'ingredient is duplicated.'}
                )
            unique.add(pk)
            if not Ingredient.objects.filter(pk=pk).exists():
                raise ValidationError(
                    {f'id {pk}': 'ingredient does not exist.'}
                )
            amount = dct.get('amount')
            if amount < 1:
                raise ValidationError(
                    {f'amount {amount}': 'the value must be greater than 0'}
                )

        return super().validate_empty_values(data)

    def create(self, validated_data):
        recipe = super().create(validated_data)
        self.save_ingredients_in_recipe(recipe)
        return recipe

    def save_ingredients_in_recipe(self, recipe):
        ingredients = self.initial_data.get('ingredients')
        recipe_ingredients = [IngredientInRecipe] * len(ingredients)
        for idx, value in enumerate(ingredients):
            recipe_ingredients[idx].objects.update_or_create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=value['id']),
                amount=value['amount']
            )


class FavoriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True
    )
    id = serializers.IntegerField(source='recipe.id', read_only=True)

    class Meta:
        model = Favorite
        fields = (
            'id',
            'user',
            'recipe',
            'name',
            'image',
            'cooking_time'
        )
        extra_kwargs = {
            'recipe': {'write_only': True},
            'user': {'write_only': True},
        }

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            if Favorite.objects.filter(
                user=attrs.get('user'),
                recipe=attrs.get('recipe')
            ).exists():
                raise serializers.ValidationError(
                    'This recipe is already in favorites'
                )
        return super().validate(attrs)


class RecipeFollowSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'cooking_time',
            'image',
        )


class FollowReadSerializer(serializers.ModelSerializer):
    """Field is_subscribed is always True."""
    recipes = RecipeFollowSerializer(many=True, read_only=True)
    recipes_count = serializers.IntegerField(read_only=True)
    is_subscribed = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )


class FollowCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='You have already subscribed to this author'
            )
        ]

    def validate(self, data):
        """Check that USER is not FOLLOWING."""
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'You can\'t subscribe to yourself'
            )
        return data


class CartCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Cart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=['user', 'recipe'],
                message='You have already this recipe in cart.'
            )
        ]
