from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from siteinfo import views

app_name = 'site_info'

urlpatterns = [
    path('about_us/',views.AboutUsView.as_view(), name='about_us')
]