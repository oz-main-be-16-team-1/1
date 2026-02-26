import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from django.core.files.base import ContentFile
from apps.transactions.models import TransactionHistory
from .models import Analysis


class AnalysisService:
    """
    분석 관련 비즈니스 로직을 담당하는 서비스 클래스
    """
    @staticmethod
    def create_transaction_analysis(user, about, analysis_type, period_start, period_end):
        # 대상 데이터 필터링 (수입/지출)
        target_type = (
            TransactionHistory.TransactionType.DEPOSIT
            if about == Analysis.AboutChoices.TOTAL_INCOME
            else TransactionHistory.TransactionType.WITHDRAW
        )

        queryset = TransactionHistory.objects.filter(
            account__user=user,
            transaction_type=target_type,
            transaction_at__date__range=[period_start, period_end]
        ).values('transaction_at', 'transaction_amount')

        if not queryset.exists():
            return None

        # pandas 가공
        df = pd.DateFrame(list(queryset))
        df['transaction_amount'] = df['transaction_amount'].astype(float)
        df['transaction_at'] = pd.to_datetime(df['transaction_at'])

        # 시각화
        plt.figure(figsize=(10, 6))

        rule = 'D' if analysis_type == Analysis.TypeChoices.DAILY else \
            'W' if analysis_type == Analysis.typeChoices.WEEKLY else 'ME'

        resampled = df.set_index('transaction_at').resample(rule)['transaction_amount'].sum()

        color = 'blue' if target_type == TransactionHistory.TransactionType.DEPOSIT else 'red'
        resampled.plot(kind='line', marker='o', color=color)

        plt.title(f"{about} Analysis")
        plt.tight_layout()

        # 이미지 생성
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()

        # 모델 인스턴스 생성 및 이미지 파일 할당
        analysis_instance = Analysis(
            user=user,
            about=about,
            type=analysis_type,
            period_start=period_start,
            period_end=period_end,
        )

        file_name = f"analysis_{user.id}_{period_start}.png"
        analysis_instance.result_image.save(
            file_name,
            ContentFile(buffer.getvalue()),
            save=True
        )

        analysis_instance.save()
        return analysis_instance