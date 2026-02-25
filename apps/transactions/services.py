from decimal import Decimal
from rest_framework.exceptions import ValidationError
from apps.transactions.models import TransactionHistory


def to_delta(tx: TransactionHistory) -> Decimal:
    amount = tx.transaction_amount or Decimal("0")
    if tx.transaction_type == "DEPOSIT":
        return amount
    if tx.transaction_type == "WITHDRAW":
        return -amount
    raise ValidationError("유효하지 않은 거래 유형입니다.")


def delta_from_values(transaction_type: str, amount: Decimal) -> Decimal:
    if transaction_type == "DEPOSIT":
        return amount
    if transaction_type == "WITHDRAW":
        return -amount
    raise ValidationError("유효하지 않은 거래 유형입니다.")

def get_queryset(self):
    queryset = TransactionHistory.objects.all().select_related(
        "account", "account__user"
    )
    params = self.request.query_params

    user_id = params.get("user_id")
    account_id = params.get("account_id")
    transaction_type = params.get("transaction_type")
    transaction_method = params.get("transaction_method")
    start_at = params.get("start_at")
    end_at = params.get("end_at")

    if user_id:
        queryset = queryset.filter(account__user_id=user_id)
    if account_id:
        queryset = queryset.filter(account_id=account_id)
    if transaction_type:
        queryset = queryset.filter(transaction_type=transaction_type)
    if transaction_method:
        queryset = queryset.filter(transaction_method=transaction_method)
    if start_at:
        queryset = queryset.filter(transaction_at__gte=start_at)
    if end_at:
        queryset = queryset.filter(transaction_at__lte=end_at)

    return queryset.order_by("-transaction_at", "-transaction_id")

def perform_create(self, serializer):
    tx = serializer.save()
    account = tx.account
    delta = to_delta(tx)
    new_balance = (account.account_balance or Decimal("0")) + delta
    if new_balance < Decimal("0"):
        raise ValidationError("잔액이 부족합니다.")

    account.account_balance = new_balance
    tx.balance_after = new_balance
    account.save(update_fields=["account_balance"])
    tx.save(update_fields=["balance_after"])


def perform_update(self, serializer):
    old_tx = self.get_object()
    account = old_tx.account
    old_delta = to_delta(old_tx)

    updated_tx = serializer.save()
    new_type = updated_tx.transaction_type
    new_amount = updated_tx.transaction_amount or Decimal("0")
    new_delta = delta_from_values(new_type, new_amount)

    new_balance = (account.account_balance or Decimal("0")) - old_delta + new_delta
    if new_balance < Decimal("0"):
        raise ValidationError("잔액이 부족합니다.")

    account.account_balance = new_balance
    updated_tx.balance_after = new_balance
    account.save(update_fields=["account_balance"])
    updated_tx.save(update_fields=["balance_after"])

def perform_destroy(self, instance):
    account = instance.account
    delta = to_delta(instance)
    new_balance = (account.account_balance or Decimal("0")) - delta
    if new_balance < Decimal("0"):
        raise ValidationError("잔액이 부족합니다.")

    instance.delete()
    account.account_balance = new_balance
    account.save(update_fields=["account_balance"])