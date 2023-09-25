from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Follow

User = get_user_model()

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "password", "first_name", "last_name")
    search_fields = ("username", "email")
    list_filter = ("username", "email")
    list_editable = ("email", "first_name", "last_name")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "following")
    search_fields = ("user", "following")
    list_filter = ("user", "following")
