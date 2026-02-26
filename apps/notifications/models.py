from django.db import models
from django.conf import settings

class Notification(models.Model):
    # 알림을 받을 사용자 (FK)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    # 알림 메시지 내용
    message = models.TextField()
    # 읽음 여부 (기본값은 읽지 않음인 False)
    is_read = models.BooleanField(default=False)
    # 알림 생성 시간
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.user.username}] {self.message[:20]}"