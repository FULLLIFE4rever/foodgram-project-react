from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Cart, Favorite, Ingredients, IngredientsRecipes,
                            Recipes, Tags)
from users.models import Follow

from .filters import IngredientsFilter, RecipeFilter
from .paginations import LimitMaxPageNumberPagination
from .permissions import IsAuthorOrAdmin
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipesAddSerializer, RecipesReadSerializer,
                          RecipeWriteSerializer, TagSerializer)

User = get_user_model()


class ListRetrieveViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientsFilter
    filter_backends = (DjangoFilterBackend,)


class TagViewSet(ListRetrieveViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class FollowViewSet(ModelViewSet):

    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk):
        user = request.user
        following = get_object_or_404(User, id=pk)

        serializer = FollowSerializer(
            following, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        Follow.objects.create(user=user, following=following)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, pk):
        user = request.user
        following = get_object_or_404(User, id=pk)
        subscription = get_object_or_404(
            Follow, user=user, following=following
        )
        subscription.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class RecipesViewSet(ModelViewSet):
    MODEL_TO_ADD_ERROR_MESSAGE = {
        Cart: "Товар уже добавлен в корзину!",
        Favorite: "Товар уже добавлен избранное!",
    }
    MODEL_TO_DELETE_ERROR_MESSAGE = {
        Cart: "Товара нет в вашей корзину!",
        Favorite: "Товара нет в вашем избранном!",
    }
    queryset = Recipes.objects.all()
    filterset_class = RecipeFilter
    pagination_class = LimitMaxPageNumberPagination
    permission_classes = (IsAuthorOrAdmin,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RecipesReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=False, methods=["get"], permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shop_list = (
            IngredientsRecipes.objects.filter(recipe__cart__user=request.user)
            .values(
                name=F("ingredients__name"),
                measurement_unit=F("ingredients__measurement_unit"),
            )
            .annotate(value=Sum("amount"))
        )

        text = "\n".join(
            [
                f"{i['name']} ({i['measurement_unit']}) - {i['value']}"
                for i in shop_list
            ]
        )

        filename = "shopping_cart.txt"
        response = HttpResponse(text, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    @action(
        detail=True, methods=["post"], permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.add_to_model(Cart, request.user, pk)

    @shopping_cart.mapping.delete
    def del_shopping_cart(self, request, pk):
        return self.delete_from_model(Cart, request.user, pk)

    @action(
        detail=True, methods=["post"], permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return self.add_to_model(Favorite, request.user, pk)

    @favorite.mapping.delete
    def del_favorite(self, request, pk):
        return self.delete_from_model(Favorite, request.user, pk)

    def add_to_model(self, model, user, id):
        model_obj = model.objects
        recipe = get_object_or_404(Recipes, id=id)
        if model_obj.filter(user=user, recipe=recipe).exists():
            return Response(
                {"error": self.MODEL_TO_ADD_ERROR_MESSAGE[model]},
                status=HTTP_400_BAD_REQUEST,
            )
        model_obj.create(user=user, recipe=recipe)
        serializer = RecipesAddSerializer(recipe)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete_from_model(self, model, user, id):
        model_obj = model.objects
        recipe = get_object_or_404(Recipes, id=id)
        if not model_obj.filter(user=user, recipe=recipe).exists():
            return Response(
                {"error": self.MODEL_TO_DELETE_ERROR_MESSAGE[model]},
                status=HTTP_400_BAD_REQUEST,
            )
        model_obj.filter(user=user, recipe=recipe).delete()
        serializer = RecipesAddSerializer(recipe)
        return Response(serializer.data, status=HTTP_204_NO_CONTENT)
