from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from django.db.models import (
    Value, Exists, Count, OuterRef, Subquery, Prefetch, Sum
)

from . import serializers
from dishes.models import Tag, Ingredient, Recipe, IngredientInRecipe
from .filters import IngredientFilter, RecipeFilter
from .permissions import RecipesPermissions
from core.pagination import LimitNumberPagination

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list', 'me'):
            return serializers.UserReadSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'subscriptions':
            return serializers.FollowReadSerializer
        if self.action == 'subscribe':
            return serializers.FollowCreateSerializer
        return serializers.UserCreateSerializer

    def get_subscriptions_queryset(self):
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
        ).all()

    def get_queryset(self):
        if self.action in ('subscriptions', 'subscribe'):
            return self.get_subscriptions_queryset()
        if self.request.user.is_anonymous:
            is_subscribed = Value(False)
        else:
            is_subscribed = Exists(
                self.request.user.follower.filter(id=OuterRef('following__id'))
            )
        return User.objects.all().annotate(is_subscribed=is_subscribed)

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Method \"DELETE\" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

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
        ['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        ['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'DELETE':
            follow = request.user.follower.filter(
                following=author
            )
            if not follow.exists():
                return Response(
                    'You are not subscribed.', status.HTTP_400_BAD_REQUEST
                )
            follow.delete()
            return Response('You unsubscribed.', status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(data={'following': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serialazer_data = serializers.FollowReadSerializer(
            self.get_queryset().first()
        ).data
        headers = self.get_success_headers(serializer.data)
        return Response(
            serialazer_data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        ['post'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data['new_password'])
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
    pagination_class = LimitNumberPagination

    def get_serializer_class(self):
        if self.action == 'favorite':
            return serializers.FavoriteSerializer
        if self.action == 'shopping_cart':
            return serializers.CartCreateSerializer
        if self.action in ('create', 'partial_update'):
            return serializers.RecipeCreateSerializer
        return serializers.RecipeReadSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            is_favorited = Value(False)
            is_in_shopping_cart = Value(False)
            is_subscribed = Value(False)
        else:
            is_favorited = Exists(user.favorites.filter(recipe=OuterRef('pk')))
            is_in_shopping_cart = Exists(
                user.cart.filter(recipe=OuterRef('pk'))
            )
            is_subscribed = Exists(
                self.request.user.follower.filter(id=OuterRef('following__id'))
            )
        queryset = Recipe.objects.annotate(
            is_favorited=is_favorited,
            is_in_shopping_cart=is_in_shopping_cart
        ).order_by('-pub_date')
        return queryset.prefetch_related(
            Prefetch(
                'author', queryset=User.objects.annotate(
                    is_subscribed=is_subscribed
                )
            )
        )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(
        ['delete', 'post'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        favorites = request.user.favorites
        if self.request.method == 'DELETE':
            favorite = favorites.filter(
                recipe=self.get_object()
            )
            if not favorite.exists():
                return Response(
                    {'This recipe was not found in favorites'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            favorite.delete()
            return Response(
                {'This recipe has been successfully deleted from favorites.'},
                status=status.HTTP_204_NO_CONTENT
            )
        if favorites.filter(recipe_id=pk).exists():
            return Response(
                {'This recipe is already in favorites'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(
            data={'recipe': pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @action(
        ['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe_id__in=Subquery(request.user.cart.all().values('recipe_id'))
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(total=Sum('amount'))
        output = '\n'.join(
            [
                ' '.join(
                    [str(value) for value in ingredient.values()]
                ) for ingredient in ingredients
            ]
        )
        return HttpResponse(
            content=output, content_type='text/plain'
        )

    @action(
        ['delete', 'post'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'DELETE':
            cart = request.user.cart.filter(
                recipe=get_object_or_404(Recipe, pk=pk)
            )
            if not cart.exists():
                return Response(
                    'There is not recipe in cart', status.HTTP_400_BAD_REQUEST
                )
            cart.delete()
            return Response('Recipe deleted.', status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(data={'recipe': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer_data = serializers.RecipeFollowSerializer(
            self.get_object()
        ).data
        return Response(
            serializer_data, status=status.HTTP_201_CREATED
        )
