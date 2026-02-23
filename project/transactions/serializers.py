from django.utils import timezone
from rest_framework import serializers

from .models import TransactionHistory


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = [
            "transaction_id",
            "account",
            "transaction_amount",
            "transaction_history",
            "transaction_type",
            "transaction_method",
            "balance_after",
            "transaction_at",
            "created_at",
        ]
        read_only_fields = ["transaction_id", "balance_after", "created_at"]

    def validate_transaction_amount(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("거래 금액은 0보다 커야 합니다.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        is_partial = bool(request and request.method == "PATCH")

        required_fields = [
            "transaction_amount",
            "transaction_type",
            "transaction_method",
        ]
        if self.instance is None and "account" not in attrs:
            raise serializers.ValidationError({"account": "계좌 정보는 필수입니다."})

        for field_name in required_fields:
            if not is_partial and self.instance is None and field_name not in attrs:
                raise serializers.ValidationError({field_name: "필수 값입니다."})

        if attrs.get("transaction_at") is None and self.instance is None:
            attrs["transaction_at"] = timezone.now()
        return attrs
