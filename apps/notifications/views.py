from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# 정확한 파일명으로 import
from .models import Notification
from .notifications_serialrizers import NotificationSerializer
from .services import mark_notification_as_read


class NotificationListView(generics.ListAPIView):
    """모든 알림 목록 출력 (읽지 않은 것 우선 정렬)"""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 유저 본인의 알림을 가져오되, 읽음 여부(False가 먼저)와 생성일 순으로 정렬
        return Notification.objects.filter(user=self.request.user).order_by(
            "is_read", "-created_at"
        )


class NotificationDetailView(generics.RetrieveAPIView):
    """알람 상세 조회 시 자동으로 읽음 처리"""

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # 1. 서비스 로직 호출 (읽음 상태 업데이트)
        mark_notification_as_read(instance.id, request.user)

        # 2. 업데이트된 데이터 반영
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)

        # 상세 내용과 함께 메시지 반환
        return Response(
            {
                "message": "알람 내용을 확인하여 읽음 처리되었습니다.",
                "data": serializer.data,
            }
        )
