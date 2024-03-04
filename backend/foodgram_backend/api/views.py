import io

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from django.db.models import Value, Count, OuterRef, Subquery, Prefetch, Sum

from . import serializers
from dishes.models import (
    Tag, Ingredient, Recipe, Favorite, IngredientInRecipe
)
from .filters import IngredientFilter, RecipeFilter
from .permissions import RecipesPermissions
from users.models import Follow

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
        return serializers.UserCreateSerializer

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [RecipesPermissions]

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return serializers.RecipeCreateSerializer
        return serializers.RecipeReadSerializer

    def get_queryset(self):
        queryset = Recipe.objects.annotate(
            is_favorited=Value(True), is_in_shopping_cart=Value(True)
        ).order_by('pub_date').all()
        return queryset

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'delete']
    permission_classes = [IsAuthenticated]
    queryset = Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        data = {"recipe": recipe_id, "user": self.request.user.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class GetFollowViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.FollowReadSerializer

    def get_queryset(self):
        authors = User.objects.filter(
            following__user=self.request.user
        ).annotate(recipes_count=Count('recipes'))
        recipes_limit = self.request.GET.get('recipes_limit')
        if not recipes_limit:
            return authors
        sub = Subquery(
            Recipe.objects.filter(author__in=authors).filter(
                author=OuterRef('author_id')
            ).order_by('pub_date').values('id')[:int(recipes_limit)]
        )
        return authors.prefetch_related(
            Prefetch('recipes', queryset=Recipe.objects.filter(id__in=sub))
        )


class DeletePostFollowViewSet(GenericAPIView):
    http_method_names = ['post', 'delete']
    permission_classes = [IsAuthenticated]

    def get_full_data(self, author_id):
        authors = User.objects.filter(id=author_id).annotate(
            recipes_count=Count('recipes')
        )
        recipes_limit = self.request.GET.get('recipes_limit')
        if not recipes_limit:
            return authors.first()
        sub = Subquery(
            Recipe.objects.filter(author__in=authors).filter(
                author=OuterRef('author_id')
            ).order_by('-id').values('id')[:int(recipes_limit)]
        )
        return authors.prefetch_related(
            Prefetch('recipes', queryset=Recipe.objects.filter(id__in=sub))
        ).first()

    def post(self, request, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        get_object_or_404(User, pk=author_id)
        data = {"following": author_id, "user": self.request.user.id}
        serializer = serializers.FollowCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serialazer_data = serializers.FollowReadSerializer(
            self.get_full_data(author_id)
        ).data
        return Response(
            serialazer_data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(
            User,
            id=self.kwargs.get('author_id'),
        )
        follow = Follow.objects.filter(
            user=self.request.user,
            following=author
        )
        if not follow.exists():
            return Response(
                'You are not subscribed.', status.HTTP_400_BAD_REQUEST
            )
        follow.delete()
        return Response('You unsubscribed.', status.HTTP_204_NO_CONTENT)


class GetCartViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        ingredients = IngredientInRecipe.objects.filter(
            id__in=Subquery(request.user.cart.all().values('recipe_id'))
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total=Sum('amount'))
        text_buffer = io.StringIO('')
        for ingredien in ingredients:
            text_buffer.write(
                '{ingredient__name} '
                '{total} '
                '{ingredient__measurement_unit}'.format(**ingredien)
            )
        return HttpResponse(
            content=text_buffer.getvalue(), content_type="text/plain"
        )


class PostCartViewSet(GenericAPIView):
    http_method_names = ['post', 'delete']
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = {
            "recipe": self.kwargs.get('recipe_id'),
            "user": self.request.user.id
        }
        serializer = serializers.CartCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer_data = serializers.RecipeFollowSerializer(
            serializer.instance.recipe
        ).data
        return Response(
            serializer_data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            id=self.kwargs.get('recipe_id')
        )
        cart = self.request.user.cart.filter(recipe=recipe)
        if not cart.exists():
            return Response(
                'There is not recipe in cart', status.HTTP_400_BAD_REQUEST
            )
        cart.delete()
        return Response('Recipe deleted.', status.HTTP_204_NO_CONTENT)
