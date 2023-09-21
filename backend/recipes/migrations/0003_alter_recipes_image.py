# Generated by Django 4.2.4 on 2023-09-18 10:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0002_remove_ingredients_slug_alter_tags_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipes",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="image_recipes/",
                verbose_name="Изображение",
            ),
        ),
    ]