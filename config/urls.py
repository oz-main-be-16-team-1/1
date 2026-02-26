"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.users.views import RegisterView, LogoutView, UserDetailView

from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import CookieTokenObtainPairView

from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserDetailView.as_view(), name='user_profile'),

    # include
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/users/", include("apps.users.urls")),
    path("api/transactions/", include("apps.transactions.urls")),
    path('api/analysis/', include('apps.analysis.urls')),

    # Token
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Swagger-ui
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Notifications
    path('api/notifications/', include('apps.notifications.urls')),
]

# 미디어 파일을 서빙하기 위한 환 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)