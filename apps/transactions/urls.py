from django.urls import path

from .views import TransactionDetailView, TransactionListCreateView

urlpatterns = [
    path("", TransactionListCreateView.as_view(), name="transaction-list-create"),
    path(
        "<int:transaction_id>/",
        TransactionDetailView.as_view(),
        name="transaction-detail",
    ),
]
