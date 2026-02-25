from decimal import Decimal

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from .models import TransactionHistory
from .serializers import TransactionSerializer
from .services import get_queryset
from .services import perform_destroy
from .services import perform_update
from .services import perform_create





class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return get_queryset(self)

    def perform_create(self, serializer):
        return perform_create(self, serializer)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransactionHistory.objects.all().select_related(
        "account", "account__user"
    )
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]
    lookup_field = "transaction_id"

    def perform_update(self, serializer):
        return perform_update(self, serializer)

    def perform_destroy(self, instance):
        return perform_destroy(self, instance)
