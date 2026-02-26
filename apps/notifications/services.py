from django.shortcuts import get_object_or_404
from .models import Notification


def mark_notification_as_read(notification_id, user):
    """
    특정 유저의 알림을 읽음 처리하는 비즈니스 로직
    """
    # 1. 해당 유저의 알림인지 확인하며 가져오기 (권한 체크 포함)
    notification = get_object_or_404(Notification, id=notification_id, user=user)

    # 2. 이미 읽었는지 확인하는 등의 정책을 추가할 수 있음
    if not notification.is_read:
        notification.is_read = True
        notification.save()

    return notification
