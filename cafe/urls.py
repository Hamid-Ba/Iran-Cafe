from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from cafe import views


router = DefaultRouter()
router.register('' , views.CafeViewSet)

app_name = "cafe"

urlpatterns = [
    path("",include(router.urls)),
    path("list/<str:province_slug>/",views.CafesListView.as_view(),name='cafes_by_province')
]