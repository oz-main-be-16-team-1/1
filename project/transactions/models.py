from django.db import models

class TransactionHistory(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "입금"
        WITHDRAW = "WITHDRAW", "출금"

    class MethodType(models.TextChoices):
        CASH = "CASH", "현금"
        BANK_TRANSFER = "BANK_TRANSFER", "계좌이체"
        AUTO_TRANSFER = "AUTO_TRANSFER", "자동이체"
        CARD = "CARD", "카드결제"

    transaction_id = models.AutoField(
        "거래 식별자", primary_key=True, db_column="거래id"
    )
    transaction_amount = models.DecimalField(
        "거래 금액", max_digits=15, decimal_places=2, null=True, db_column="거래금액"
    )
    transaction_history = models.CharField(
        "거래 내역", max_length=255, null=True, db_column="거래내역"
    )
    transaction_type = models.CharField(
        "입출금 타입",
        max_length=10,
        choices=TransactionType.choices,
        null=True,
        db_column="입출금타입",
    )
    transaction_method = models.CharField(
        "거래 방식",
        max_length=20,
        choices=MethodType.choices,
        null=True,
        db_column="거래타입"
    )
    balance_after = models.DecimalField(
        "거래 후 잔액", max_digits=15, decimal_places=2, null=True, db_column="거래후잔액"
    )
    transaction_at = models.DateTimeField(
        "거래 일시", null=True, db_column="거래일시"
    )
    created_at = models.DateTimeField(
        "데이터 생성일", auto_now_add=True, db_column="created_at"
    )

    account = models.ForeignKey(
        "accounts.Account",
        on_delete=models.CASCADE,
        db_column="계좌id",
        related_name="transactions",
        verbose_name="연결 계좌"
    )

    class Meta:
        db_table = "transaction_history"
        verbose_name = "거래 내역"
        verbose_name_plural = "거래 내역 목록"

    def __str__(self):
        # 예: [입금] 50,000원 (2026-02-23)
        return f"[{self.get_transaction_type_display()}] {self.transaction_amount}원"