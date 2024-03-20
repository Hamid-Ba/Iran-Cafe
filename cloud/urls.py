from django.urls import (
    path,
)

from cloud import views

app_name = "cloud"

urlpatterns = [
    path(
        "cloud/",
        views.CloudyCustomerViewSet.as_view({"get": "retrieve", "post": "create"}),
        name="cloudy",
    ),
]
