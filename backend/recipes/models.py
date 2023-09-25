from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Tags(models.Model):
    """Модель тегов"""

    name = models.TextField(
        verbose_name="Назвение тега", max_length=200, unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name="Цвет тега в HEX",
        validators=[
            RegexValidator(
                "^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$",
                message=("Поле не содержит цвет в формате HEX"),
            )
        ],
        unique=True,
    )
    slug = models.CharField(verbose_name="Уникальное название", max_length=200)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Модель ингридиентов"""

    name = models.TextField(
        verbose_name="Назвение ингридиента", max_length=100
    )
    measurement_unit = models.CharField(
        max_length=20, verbose_name="Система СИ"
    )

    class Meta:
        ordering = ("measurement_unit",)

    def __str__(self):
        return f"{self.name},{self.measurement_unit}"


class Recipes(models.Model):
    """Модель рецептов"""

    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name="Ингредиенты",
        through="IngredientsRecipes",
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name="Теги",
        blank=True,
        db_index=True,
        related_name="tags",
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="image_recipes/",
        null=True,
        blank=True,
    )
    name = models.TextField(
        verbose_name="Название рецепта",
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    text = models.TextField(
        verbose_name="Рецепт",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления(минуты)",
        validators=[MinValueValidator(5, "Время должно быть от 5 минуты.")],
    )

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name


class IngredientsRecipes(models.Model):
    """Промежуточная модель объединения
    ингридиентов и рецептов"""

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name="ingredient",
        verbose_name="Рецепт",
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name="ingredient",
        verbose_name="Ингредиент",
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Количество в рецепте",
        validators=[MinValueValidator(1, "Минимальное значение 1")],
    )


class Favorite(models.Model):
    """Модель избранного"""

    user = models.ForeignKey(
        User,
        related_name="favorite",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name="favorite",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Рецепт",
    )

    class Meta:
        constraints = (
            UniqueConstraint(fields=["user", "recipe"], name="user-recipe"),
        )


class Cart(models.Model):
    """Модель корзины"""

    user = models.ForeignKey(
        User,
        related_name="cart",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name="cart",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Рецепт",
    )

    class Meta:
        constraints = (
            UniqueConstraint(fields=["user", "recipe"], name="user-cart"),
        )
