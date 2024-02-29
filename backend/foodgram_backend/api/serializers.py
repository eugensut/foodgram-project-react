import base64

from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile

from users.models import User
from dishes.models import Tag, Ingredient, IngredientInRecipe, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class UserReadSerializer(serializers.ModelSerializer):
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

    def validate_ingredients(self, value):
        for dct in value:
            pk = dct.get('id')
            if not Ingredient.objects.filter(pk=pk).exists():
                raise ValidationError(
                    {f'id {pk}': 'does not exist.'}
                )
        return value

    def create(self, validated_data):
        recipe = super().create(validated_data)
        self.save_ingredients_in_recipe(recipe)
        return recipe
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def save_ingredients_in_recipe(self, recipe):
        ingredients = self.initial_data.get('ingredients')
        recipe_ingredients = [IngredientInRecipe] * len(ingredients)
        for idx, value in enumerate(ingredients):
            recipe_ingredients[idx].objects.update_or_create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=value['id']),
                amount=value['amount']
            )

