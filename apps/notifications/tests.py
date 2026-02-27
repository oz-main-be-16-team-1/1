from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Notification

# User 모델 가져오기
User = get_user_model()


class NotificationAPITests(APITestCase):
    def setUp(self):
        """테스트 시작 전 기초 데이터 설정"""
        self.user = User.objects.create_user(
            user_email="testuser@example.com",
            password="testpassword123",
            user_name="테스트유저",
            user_nickname="테스터1",
        )
        self.client.force_authenticate(user=self.user)

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
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["is_read"], False)

    def test_notification_detail_and_auto_read(self):
        """Mission 2: 상세 조회 시 자동 읽음 처리 테스트"""
        url = reverse("notification-detail", kwargs={"pk": self.unread_notification.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.unread_notification.refresh_from_db()
        self.assertTrue(self.unread_notification.is_read)

    def test_notification_access_denied_for_other_user(self):
        """보안 테스트: 다른 유저의 알람을 볼 수 없는지 확인"""
        # 1. 다른 유저 생성 (변수 사용함)
        other_user = User.objects.create_user(
            user_email="other@example.com",
            password="password",
            user_name="다른유저",
            user_nickname="테스터2",
            user_phone='01000003323'
        )

        # 2. 생성한 other_user 변수를 사용하여 알람 생성
        notif = Notification.objects.create(user=other_user, message="다른 사람 것")

        # 3. 생성한 notif 변수를 사용하여 URL 생성
        url = reverse("notification-detail", kwargs={"pk": notif.pk})
        response = self.client.get(url)

        # 4. status 모듈을 사용하여 상태 코드 검증
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
