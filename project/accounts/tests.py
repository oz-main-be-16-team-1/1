from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from accounts.models import Account
from transactions.models import TransactionHistory


class AccountTransactionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            user_email = 'tester@test.com',
            password = '1q2w3e4r!@',
            user_nickname ="테스터"
        )

        self.client.force_authenticate(user=self.user)

        self.account = Account.objects.create(
            user = self.user,
            bank_code='001',
            account_number = '123-123-123',
            account_type=Account.AccountType.CHECKING,
            account_balance=10000.00
        )


    def test_create_account(self):
        """계좌 생성 테스트"""
        url = reverse('account-list-create')
        data = {
            "bank_code": "002",
            "account_number": "987-654-321",
            "account_type": "SAVINGS",
            "account_balance": 5000.00,
            "user": self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)

    def test_read_account(self):
        """계좌 조회 테스트"""
        url = reverse('account-detail', kwargs={'account_id': self.account.account_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['account_number'], "123-123-123")


    def test_create_transaction(self):
        """입출금 내역 생성 테스트"""
        url = reverse('transaction-list-create')
        data = {
            "account": self.account.account_id,
            "transaction_amount": 2000.00,
            "transaction_history": "볼펜 결제",
            "transaction_type": "WITHDRAW",
            "transaction_method": "CARD",
            "balance_after": 8000.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TransactionHistory.objects.filter(account=self.account).count(), 1)

    def test_get_transaction_history(self):
        """특정 계좌의 거래 내역 조회 테스트"""
        TransactionHistory.objects.create(
            account = self.account,
            transaction_amount = 500.00,
            transaction_type = "DEPOSIT",
            transaction_method = "CASH"
        )
        url = reverse('transaction-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)