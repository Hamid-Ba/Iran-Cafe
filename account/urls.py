"""
Account Module Mapper
"""
from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from account import views

router = DefaultRouter()
router.register("auth",views.AuthenticationViewSet , basename='auth')

app_name = "account"

urlpatterns = [
    path("",include(router.urls)),
    path("token/", views.AuthTokenView.as_view() , name = "token"),
]