from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Analysis(models.Model):
    class AboutChoices(models.TextChoices):
        TOTAL_SPENDING = "TOTAL_SPENDING", "총 지출"
        TOTAL_INCOME = "TOTAL_INCOME", "총 수입"

    class TypeChoices(models.TextChoices):
        DAILY = "DAILY" ,"일간"
        WEEKLY = "WEEKLY", "주간"
        MONTHLY = "MONTHLY", "월간"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analyses',
        verbose_name='유저',
    )

    about = models.CharField(
        max_length=30,
        choices = AboutChoices.choices,
        verbose_name='분석대상',
    )

    type = models.CharField(
        max_length=20,
        choices = TypeChoices.choices,
        verbose_name='분석 기간 유형'
    )

    period_start = models.DateField(verbose_name="분석 시작일")
    period_end = models.DateField(verbose_name="분석 종료일")
    description = models.TextField(blank=True, verbose_name="설명")
    result_image = models.ImageField(
        upload_to='analysis/',
        blank=True,
        null=True,
        verbose_name="결과 이미지"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis'
        verbose_name ='분석'
        verbose_name_plural = '분석 목록'

    def clean(self):
        if self.period_start >= self.period_end:
            raise ValidationError("period_start must be before period_end")