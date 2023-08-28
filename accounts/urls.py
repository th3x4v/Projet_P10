from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers

from accounts.views import RegisterView, UserViewSet


router = routers.SimpleRouter()

router.register(r"users", UserViewSet)
users_router = routers.NestedSimpleRouter(router, r"users", lookup="user")


urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(users_router.urls)),
    path("", include(router.urls)),
]
