from django.urls import path

from queries import views

app_name = "queries"

urlpatterns = [
    path("order/", views.OrderQueryView.as_view(), name="order"),
    path(
        "loyal_customers/<int:number>/",
        views.LoyalCustomers.as_view(),
        name="loyal_customers",
    ),
]
