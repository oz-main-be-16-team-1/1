from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "account_id",
            "user",
            "bank_code",
            "account_number",
            "account_type",
            "account_balance",
            "created_at",
        ]
        read_only_fields = ["account_id", "created_at"]
