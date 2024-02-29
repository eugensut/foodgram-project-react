from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from django.db.models import Value

from . import serializers
from dishes.models import Tag, Ingredient, Recipe
from .custom_filters import IngredientFilter

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list', 'me'):
            return serializers.UserReadSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        return serializers.CreateUserSerializer

    @action(
            ['get'],
            detail=False,
            permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(
            request.user
        )
        return Response(serializer.data)

    @action(
            ['post'],
            detail=False,
            permission_classes=[IsAuthenticated]
    )
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return serializers.RecipeCreateSerializer
        return serializers.RecipeReadSerializer
  
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny(), ]
        return [IsAuthenticated(), ]

    def get_queryset(self):
        queryset = Recipe.objects.annotate(
            is_favorited=Value(True), is_in_shopping_cart=Value(True)
        ).all()
        return queryset
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
