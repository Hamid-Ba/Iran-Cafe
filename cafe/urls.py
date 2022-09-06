from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from cafe import views


router = DefaultRouter()
router.register('cafe' , views.CafeViewSet , basename = 'cafe')

app_name = "cafe"

urlpatterns = [
    path("",include(router.urls)),
]