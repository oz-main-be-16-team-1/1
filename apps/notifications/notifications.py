from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .notifications_serialrizers import NotificationSerializer

class UnreadNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 요청을 보낸 유저(self.request.user)의 알림 중
        # 읽지 않은(is_read=False) 알림만 필터링하여 반환
        return Notification.objects.filter(
            user=self.request.user,
            is_read=False
        ).order_by('-created_at')