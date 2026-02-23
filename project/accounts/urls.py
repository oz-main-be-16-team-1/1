from django.urls import path

from .views import AccountDetailView, AccountListCreateView

urlpatterns = [
    path("", AccountListCreateView.as_view(), name="account-list-create"),
    path("<int:account_id>/", AccountDetailView.as_view(), name="account-detail"),
]
