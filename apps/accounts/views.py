from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Account
from .serializers import AccountSerializer


class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all().select_related("user").order_by("-account_id")
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]


class AccountDetailView(generics.RetrieveDestroyAPIView):
    queryset = Account.objects.all().select_related("user")
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]
    lookup_field = "account_id"
