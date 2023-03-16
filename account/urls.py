"""
Account Module Mapper
"""
from django.urls import (
    path,
)

from account import views

# router = DefaultRouter()
# router.register("auth",views.AuthenticationViewSet , basename='auth')

app_name = "account"

urlpatterns = [
    # path("",include(router.urls)),
    path("login_or_register/", views.LoginOrRegisterView.as_view(), name="otp"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("token/", views.AuthTokenView.as_view(), name="token"),
    path("me/", views.UserView.as_view(), name="me"),
]
