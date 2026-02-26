from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Analysis(models.Model):
    class AboutChoices(models.TextChoices):
        TOTAL_SPENDING = "TOTAL_SPENDING", "총 지출"
        TOTAL_INCOME = "TOTAL_INCOME", "총 수입"

    class TypeChoices(models.TextChoices):
        DAILY = "DAILY", "일간"
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
        choices=AboutChoices.choices,
        verbose_name='분석대상',
    )

    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        verbose_name='분석 기간 유형'
    )

    period_start = models.DateField(verbose_name="분석 시작일")
    period_end = models.DateField(verbose_name="분석 종료일")
    description = models.TextField(blank=True, verbose_name="설명")

    result_image = models.ImageField(
        upload_to='analysis/%Y/%m/',  # 날짜별로 폴더를 나눠 저장하면 관리가 편합니다
        blank=True,
        null=True,
        verbose_name="결과 이미지"
    )

    # models.DateTimeField 형식으로 통일
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis'
        verbose_name = '분석'
        verbose_name_plural = '분석 목록'
        ordering = ['-created_at']  # 최신 분석이 먼저 나오도록 정렬 추가

    def __str__(self):
        return f"[{self.get_type_display()}] {self.user.username} - {self.about}"

    def clean(self):
        # 데이터 정합성 검사는 모델에 남겨둡니다. (서비스에서도 호출 가능)
        if self.period_start and self.period_end:
            if self.period_start >= self.period_end:
                raise ValidationError("분석 시작일은 종료일보다 빨라야 합니다.")