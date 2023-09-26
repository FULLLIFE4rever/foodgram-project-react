from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from recipes.models import (Cart, Favorite, Ingredients, IngredientsRecipes,
                            Recipes, Tags)
from users.models import Follow

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()


class UserCreateSerializer(UserCreateSerializer):
    """Сериализация объектов типа User. Создание пользователя."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )


class UserSerializer(UserSerializer):
    """Сериализация объектов типа User. Просмотр пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
        read_only_fields = ("is_subscribed",)

    def get_is_subscribed(self, obj):
        request = self.context.get("request")

        return (
            request
            and request.user.is_authenticated
            and request.user.follower.filter(following=obj.id).exists()
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов"""

    class Meta:
        fields = "__all__"
        model = Tags


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""

    class Meta:
        fields = ("id", "name", "measurement_unit")
        model = Ingredients


class IngredientRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецепте"""

    id = serializers.ReadOnlyField(source="ingredients.id")
    name = serializers.ReadOnlyField(source="ingredients.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredients.measurement_unit"
    )

    class Meta:
        fields = ("id", "name", "amount", "measurement_unit")
        model = IngredientsRecipes


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientsRecipes
        fields = ("id", "amount")


class RecipesAddSerializer(ImageSerializer):
    class Meta:
        model = Recipes
        fields = ("id", "name", "image", "cooking_time")


class RecipesReadSerializer(ImageSerializer):
    """Сериализатор рецептов"""

    is_favorited = serializers.SerializerMethodField()
    is_in_shoping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipesSerializer(
        many=True, read_only=True, source="ingredient"
    )
    author = UserSerializer()

    class Meta:
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shoping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        model = Recipes

    def get_is_favorited(self, obj):
        """Проверка рецепт в избранном"""
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return request.user.favorite.filter(recipe=obj).exists()

    def get_is_in_shoping_cart(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return request.user.cart.filter(recipe=obj).exists()


class RecipeWriteSerializer(ImageSerializer):
    """Сериализатор для записи рецептов"""

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tags.objects.all()
    )
    ingredients = AddIngredientSerializer(many=True)

    class Meta:
        fields = (
            "tags",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        model = Recipes

    def validate_cooking_time(self, value):
        if value < 5:
            raise serializers.ValidationError(
                "Время приготовления должно быть не менее 5 минут!"
            )
        return value

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientsRecipes.objects.create(
                recipe=recipe,
                ingredients_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if "tags" in validated_data:
            instance.tags.set(validated_data.pop("tags"))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipesReadSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок"""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipes.objects.all())

    class Meta:
        model = Cart
        fields = ("user", "recipe")

    def validate(self, obj):
        """Проверка на добавление в корзину"""
        user = self.context["request"].user
        recipe = obj["recipe"]
        cart = user.list.filter(recipe=recipe).exists()
        if self.context.get("request").method == "POST" and cart:
            raise serializers.ValidationError(
                "Этот рецепт уже в списке покупок."
            )
        if self.context.get("request").method == "DELETE" and not cart:
            raise serializers.ValidationError(
                "Этот рецепт ещё не в списке покупок."
            )
        return obj


class RecipeFollowSerializer(serializers.ModelSerializer):
    """
    Сериализация объектов типа Recipes.
    Добавление в избранное/список покупок.
    """

    class Meta:
        model = Recipes
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("id", "name", "image", "cooking_time")


class FollowSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Follow. Подписки."""

    email = serializers.ReadOnlyField(source="following.email")
    username = serializers.ReadOnlyField(source="following.username")
    first_name = serializers.ReadOnlyField(source="following.first_name")
    last_name = serializers.ReadOnlyField(source="following.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipe = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipe",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.follower.filter(following=obj.id).exists()

    def get_recipe(self, obj):
        """Получение рецептов автора."""
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        queryset = obj.recipes.all()
        if limit:
            queryset = queryset[: int(limit)]
        return RecipeFollowSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()


class FollowCheckSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Follow. Подписки."""

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        following = self.instance
        user = self.context.get("request").user
        check_follow = Follow.objects.filter(
            following=following, user=user
        ).exists()
        method = self.context.get("request").method
        if user == following:
            raise serializers.ValidationError(
                detail="Вы не можете подписаться на самого себя!",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if check_follow and method == "POST":
            raise serializers.ValidationError(
                detail="Вы уже подписаны на этого пользователя!",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if check_follow and method == "DELETE":
            raise serializers.ValidationError(
                detail="Вы не подписаны на этого пользователя!",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов"""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipes.objects.all())

    class Meta:
        model = Favorite
        fields = ("user", "recipe")

    def validate(self, obj):
        """Проверка на добавление в корзину"""
        user = self.context["request"].user
        recipe = obj["recipe"]
        favorite = user.list.filter(recipe=recipe).exists()
        if self.context.get("request").method == "POST" and favorite:
            raise serializers.ValidationError(
                "Этот рецепт уже в списке избранного."
            )
        if self.context.get("request").method == "DELETE" and not favorite:
            raise serializers.ValidationError(
                "Этот рецепт ещё не в списке избранного."
            )
        return obj
