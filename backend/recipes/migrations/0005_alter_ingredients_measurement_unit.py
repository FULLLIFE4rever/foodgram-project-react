# Generated by Django 4.2.4 on 2023-09-23 01:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0004_alter_recipes_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredients",
            name="measurement_unit",
            field=models.CharField(max_length=20, verbose_name="Система СИ"),
        ),
    ]
