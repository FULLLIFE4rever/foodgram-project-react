# Generated by Django 4.2.4 on 2023-09-16 19:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_follow_self_subscription_prohibited"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="follow",
            name="user-author",
        ),
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.UniqueConstraint(
                fields=("user", "following"), name="user-following"
            ),
        ),
    ]
