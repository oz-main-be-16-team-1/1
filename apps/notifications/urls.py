from django.urls import path
from .views import NotificationListView, NotificationDetailView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    # 상세 페이지(예: /api/notifications/2/)에 접속하면 읽음 처리가 됩니다.
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]