from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import FollowViewSet, IngredientViewSet, RecipesViewSet, TagViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("tags", TagViewSet)
router.register("recipes", RecipesViewSet)
# router.register("users", FollowViewSet, basename="users")

router_user = routers.DefaultRouter()
router_user.register("users", FollowViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("", include(router_user.urls)),
    path("auth/", include("djoser.urls.authtoken")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
