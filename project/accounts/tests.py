from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from accounts.models import Account



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


