from django_filters.rest_framework import CharFilter, FilterSet, filters

from recipes.models import Ingredients, Recipes, Tags


class IngredientsFilter(FilterSet):
    """Класс для фильтрации обьектов Ingredients."""

    name = CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Ingredients
        fields = ("name",)


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tags.objects.all(),
    )

    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart"
    )

    class Meta:
        model = Recipes
        fields = (
            "tags",
            "author",
        )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_anonymous:
            return queryset
        return queryset.filter(favorite__user=user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_anonymous:
            return queryset
        return queryset.filter(cart__user=user)
