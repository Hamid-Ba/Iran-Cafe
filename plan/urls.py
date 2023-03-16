from django.urls import (
    path,
)

from plan import views

app_name = "plan"

urlpatterns = [path("plans/", views.PlanListView.as_view(), name="plans")]
