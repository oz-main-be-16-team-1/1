from django.db import models


class Account(models.Model):
    class AccountType(models.TextChoices):
        CHECKING = "CHECKING", "입출금"
        SAVINGS = "SAVINGS", "예금"
        FIXED = "FIXED", "정기예금"
        INSTALLMENT = "INSTALLMENT", "적금"

    account_id = models.AutoField("계좌 식별자", primary_key=True, db_column="계좌id")
    bank_code = models.CharField("은행 코드", max_length=3, db_column="은행코드")
    account_number = models.CharField("계좌 번호", max_length=30, db_column="계좌번호", unique=True)

    account_type = models.CharField(
        "계좌 유형", max_length=20, choices=AccountType.choices, db_column="계좌유형"
    )

    account_balance = models.DecimalField(
        "계좌 잔액", max_digits=15, decimal_places=2, default=0.00, db_column="계좌잔액"
    )

    created_at = models.DateTimeField("생성 일시", auto_now_add=True, db_column="생성일시")

    user = models.ForeignKey(
        "apps.users.User",
        on_delete=models.CASCADE,
        db_column="유저id",
        related_name="accounts",
        verbose_name="소유자",
    )

    class Meta:
        db_table = "accounts"
        verbose_name = "계좌"
        verbose_name_plural = "계좌 목록"

    def __str__(self):
        return f"{self.user.user_nickname}의 {self.account_number}"
