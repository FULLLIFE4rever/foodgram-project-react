from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ("id",)
        constraints = (
            models.UniqueConstraint(
                fields=["user", "following"], name="user-following"
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("following")),
                name="self_subscription_prohibited",
            ),
        )
