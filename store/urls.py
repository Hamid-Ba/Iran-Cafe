from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include
)

from store import views

router = DefaultRouter()
router.register("products", views.ProductApiView)
router.register("category", views.CategoryApiView)

app_name = "store"

urlpatterns = [
    path("" , include(router.urls)),
]