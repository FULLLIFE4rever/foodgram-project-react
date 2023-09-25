from django.contrib import admin

from .models import (Cart, Favorite, Ingredients, IngredientsRecipes, Recipes,
                     Tags)


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "slug",
        "name",
        "color",
    )
    search_fields = (
        "slug",
        "name",
    )
    list_filter = (
        "slug",
        "name",
    )
    list_editable = ("slug", "name", "color")


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    LIST_OF_COLOMNS = ("name", "measurement_unit")
    list_display = LIST_OF_COLOMNS
    search_fields = LIST_OF_COLOMNS
    list_filter = ("name",)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "author",
    )
    list_editable = (
        "name",
        "author",
    )
    search_fields = ("author", "name", "tags", "favotite_count")
    readonly_fields = ("favotite_count",)
    list_filter = ("author", "name", "tags")

    def favotite_count(self, obj):
        return obj.favorite.count()


@admin.register(IngredientsRecipes)
class IngredientsRecipesAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "ingredients", "amount")
    list_editable = ("recipe", "ingredients", "amount")
    list_filter = ("recipe", "ingredients")


@admin.register(Favorite)
class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    list_editable = ("user", "recipe")
    list_filter = ("user", "recipe")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    list_editable = ("user", "recipe")
    list_filter = ("user", "recipe")
