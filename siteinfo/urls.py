from django.urls import (
    path,
)

from siteinfo import views

app_name = "site_info"

urlpatterns = [
    path("about_us/", views.AboutUsView.as_view(), name="about_us"),
    path("contact_us/", views.ContactUsView.as_view(), name="contact_us"),
    path("ci_cd/", views.CI_CDView.as_view(), name="test_ci_cd"),
]
