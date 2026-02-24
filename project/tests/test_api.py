from decimal import Decimal

from accounts.models import Account
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from transactions.models import TransactionHistory
from users.models import User


class AccountTransactionAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            user_email="test@example.com",
            user_name="테스터",
            user_nickname="tester1",
            user_pw="pw1234",
            user_phone="01012345678",
        )

    def test_account_create_list_delete_and_immutable(self):
        list_url = reverse("account-list-create")
        payload1 = {
            "user": self.user.user_id,
            "bank_code": "090",
            "account_number": "123-456-7890",
            "account_type": "CHECKING",
            "account_balance": "1000.00",
        }
        payload2 = {
            "user": self.user.user_id,
            "bank_code": "004",
            "account_number": "333-444-5555",
            "account_type": "SAVINGS",
            "account_balance": "500.00",
        }

        create1 = self.client.post(list_url, payload1, format="json")
        create2 = self.client.post(list_url, payload2, format="json")
        self.assertEqual(create1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create2.status_code, status.HTTP_201_CREATED)

        listed = self.client.get(list_url)
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listed.data), 2)

        detail_url = reverse(
            "account-detail", kwargs={"account_id": create1.data["account_id"]}
        )
        patch_response = self.client.patch(
            detail_url, {"bank_code": "088"}, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 1)

    def test_transaction_create_list_filter_update_delete(self):
        account = Account.objects.create(
            user=self.user,
            bank_code="090",
            account_number="999-888-7777",
            account_type="CHECKING",
            account_balance=Decimal("1000.00"),
        )

        list_url = reverse("transaction-list-create")
        deposit_payload = {
            "account": account.account_id,
            "transaction_amount": "500.00",
            "transaction_history": "월급 입금",
            "transaction_type": TransactionHistory.TransactionType.DEPOSIT,
            "transaction_method": TransactionHistory.MethodType.CASH,
        }
        withdraw_payload = {
            "account": account.account_id,
            "transaction_amount": "200.00",
            "transaction_history": "생활비 출금",
            "transaction_type": TransactionHistory.TransactionType.WITHDRAW,
            "transaction_method": TransactionHistory.MethodType.CARD,
        }

        deposit_response = self.client.post(list_url, deposit_payload, format="json")
        withdraw_response = self.client.post(list_url, withdraw_payload, format="json")
        self.assertEqual(deposit_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(withdraw_response.status_code, status.HTTP_201_CREATED)

        account.refresh_from_db()
        self.assertEqual(account.account_balance, Decimal("1300.00"))

        filtered = self.client.get(
            f"{list_url}?account_id={account.account_id}&transaction_type=WITHDRAW"
        )
        self.assertEqual(filtered.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filtered.data), 1)
        self.assertEqual(filtered.data[0]["transaction_type"], "WITHDRAW")

        for required in [
            "account",
            "transaction_type",
            "transaction_amount",
            "transaction_at",
        ]:
            self.assertIn(required, filtered.data[0])

        update_url = reverse(
            "transaction-detail",
            kwargs={"transaction_id": withdraw_response.data["transaction_id"]},
        )
        patch_response = self.client.patch(
            update_url, {"transaction_amount": "100.00"}, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        account.refresh_from_db()
        self.assertEqual(account.account_balance, Decimal("1400.00"))

        deposit_delete_url = reverse(
            "transaction-detail",
            kwargs={"transaction_id": deposit_response.data["transaction_id"]},
        )
        delete_response = self.client.delete(deposit_delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        account.refresh_from_db()
        self.assertEqual(account.account_balance, Decimal("900.00"))
