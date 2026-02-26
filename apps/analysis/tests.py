import os
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.test import TestCase

from apps.accounts.models import Account
from apps.analysis.analysis_services import AnalysisService
from .models import Analysis
from apps.transactions.models import TransactionHistory

User = get_user_model()

class AnalysisTestCase(TestCase):
    def setUp(self):
        # 테스트 유저 생성
        self.user = User.objects.create_user(
            user_email='tester@test.com',
            password='12345678',
            user_nickname='테스터'
        )

        # 테스트 계좌 생성
        self.account = Account.objects.create(
            user=self.user,
            bank_code='001',
            account_number='123-456-789-000',
            account_type=Account.AccountType.CHECKING,
            account_balance=10000.00,
        )

        # 테스트 거래 데이터 생성
        self.today = date.today()
        for i in range(5):
            TransactionHistory.objects.create(
                account=self.account,
                transaction_amount=1000.00,
                transaction_type=TransactionHistory.TransactionType.WITHDRAW,
                transaction_at=self.today - timedelta(days=1)
            )

    def tearDown(self):
        # 테스트 종류 후 임시 새성된 미디어 파일 삭제
        if os.path.exists('/tmp/django_test_media'):
            import shutil
            shutil.rmtree('/tmp/django_test_media')

    def test_create_transaction_analysis_success(self):
        # 실행
        analysis = AnalysisService.create_transaction_analysis(
            user=self.user,
            about=Analysis.AboutChoices.TOTAL_SPENDING,
            analysis_type=Analysis.TypeChoices.DAILY,
            period_start=self.today - timedelta(days=7),
            period_end=self.today
        )

        #검증 객체가 생성되었는가?
        self.assertIsNotNone(analysis)
        self.assertIsInstance(analysis, Analysis)

        #검증 데이터가 정확한가?
        self.assertEqual(analysis.user, self.user)
        self.assertEqual(analysis.about, Analysis.AboutChoices.TOTAL_SPENDING)

        #검증 이미지 파일이 실제로 저장되었는가?
        self.assertTrue(analysis.result_image.name.startswith('analysis/'))
        self.assertTrue(default_storage.exists(analysis.result_image.name))

    def test_analysis_no_data(self):
        """
        거래 내역이 없는 기간에 대한 분석 요청 시 None을 반환하는지 테스트
        """
        future_date = self.today + timedelta(days=10)

        analysis = AnalysisService.create_transaction_analysis(
            user=self.user,
            about=Analysis.AboutChoices.TOTAL_SPENDING,
            analysis_type=Analysis.TypeChoices.DAILY,
            period_start=future_date,
            period_end=future_date + timedelta(days=7)
        )

        # 검증 데이터가 없으면 None이어야 한다.
        self.assertIsNone(analysis)