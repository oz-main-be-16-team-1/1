from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Notification

User = get_user_model()


class NotificationAPITests(APITestCase):
    def setUp(self):
        """테스트 시작 전 기초 데이터 설정"""
        # 필수 필드인 user_name과 user_nickname을 명확히 전달합니다.
        self.user = User.objects.create_user(
            user_email="testuser@example.com",
            password="testpassword123",
            user_name="테스트유저",
            user_nickname="테스터1",
        )
        self.client.force_authenticate(user=self.user)

        # 테스트용 알림 데이터 생성
        self.unread_notification = Notification.objects.create(
            user=self.user, message="읽지 않은 알람입니다.", is_read=False
        )
        self.read_notification = Notification.objects.create(
            user=self.user, message="이미 읽은 알람입니다.", is_read=True
        )

    def test_notification_list_view(self):
        """Mission 1: 알람 리스트 조회 테스트"""
        url = reverse("notification-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 생성한 알람 2개가 모두 응답에 포함되는지 확인
        self.assertEqual(len(response.data), 2)
        # 안 읽은 것이 먼저 오는지 확인 (정렬 로직에 따라)
        self.assertEqual(response.data[0]["is_read"], False)

    def test_notification_detail_and_auto_read(self):
        """Mission 2: 상세 조회 시 자동 읽음 처리 테스트"""
        url = reverse("notification-detail", kwargs={"pk": self.unread_notification.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 실제 DB 값이 True로 변경되었는지 검증
        self.unread_notification.refresh_from_db()
        self.assertTrue(self.unread_notification.is_read)

    def test_notification_access_denied_for_other_user(self):
        """보안 테스트: 다른 유저의 알람을 볼 수 없는지 확인"""
        # 다른 유저 생성 시에도 고유한 닉네임 부여
        other_user = User.objects.create_user(
            user_email="other@example.com",
            password="password",
            user_name="다른유저",
            user_nickname="테스터2",
        )
        other_notification = Notification.objects.create
