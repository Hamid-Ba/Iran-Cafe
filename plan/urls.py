from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from plan import views

app_name = 'plan'

urlpatterns = [
    path('plans/' , views.PlanListView.as_view(), name='plans')
]