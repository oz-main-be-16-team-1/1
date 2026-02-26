import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Analysis
from apps.transactions.models import TransactionHistory


class TransactionAnalyzer:
    def __init__(self, user, about, analysis_type, period_start, period_end):
        self.user = user
        self.about = about
        self.analysis_type = analysis_type
        self.period_start = period_start
        self.period_end = period_end

    def analyze(self):
        target_type = (
            TransactionHistory.TransactionType.DEPOSIT
            if self.about == Analysis.AboutChoices.TOTAL_INCOME
            else TransactionHistory.TransactionType.WITHDRAW
        )

        queryset = TransactionHistory.objects.filter(
            account__user=self.user,
            transaction_type=target_type,
            created_at__date__range=[self.period_start, self.period_end]
        ).values('transaction_at', 'transaction_amount')

        if not queryset.exists():
            return None

        df = pd.DataFrame(list(queryset))
        df['transaction_amount'] = df['transaction_amount'].astype(float)
        df['transaction_at'] = pd.to_datetime(df['transaction_at'])

        plt.figure(figsize=(10, 6))

        if self.analysis_type == Analysis.TypeChoices.DAILY:
            resampled = df.set_index('transaction_at').resample('D')['transaction_amount'].sum()
        elif self.analysis_type == Analysis.TypeChoices.WEEKLY:
            resampled = df.set_index('transaction_at').resample('W')['transaction_amount'].sum()
        else:
            resampled = df.set_index('transaction_at').resample('ME')['transaction_amount'].sum()

        color = 'blue' if target_type == TransactionHistory.TransactionType.DEPOSIT else 'red'
        resampled.plot(kind='line', market='o', linestyle='-', color=color)

        plt.title(f"{self.about} Analysis ({self.analysis_type})")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()

        analysis_obj = Analysis(
            user=self.user,
            about=self.about,
            type=self.analysis_type,
            period_start=self.period_start,
            period_end=self.period_end,
            description=f"{self.user.username}님의 {self.period_start} ~ {self.period_end} 리포트"
        )

        image_name = f"analysis_{self.user.id}_{self.period_start}.png"
        analysis_obj.result_image.save(
            image_name,
            ContentFile(buffer.getvalue()),
            save=False
        )

        analysis_obj.save()
        return analysis_obj