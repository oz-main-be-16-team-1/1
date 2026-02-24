from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('user_email', 'user_name', 'user_nickname', 'is_staff', 'is_active')

    # 1. 검색 기능 설정 (이메일, 닉네임, 휴대폰번호)
    search_fields = ('user_email', 'user_nickname', 'user_phone')

    # 2. 필터 설정 (관리자 계정 여부, 계정 활성화 상태)
    list_filter = ('is_staff', 'is_active')

    # 3. 읽기 전용 필드 설정 (어드민 여부는 관리자가 읽을 수만 있게)
    readonly_fields = ('is_superuser', 'last_login', 'created_at')

    # 기존 UserAdmin의 설정을 유지하면서 커스텀 필드를 추가합니다.
    fieldsets = (
        (None, {'fields': ('user_email', 'password')}),
        ('개인정보', {'fields': ('user_name', 'user_nickname', 'user_phone')}),
        ('권한', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('중요일정', {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_email', 'user_nickname', 'password'),
        }),
    )

    # 정렬 기준
    ordering = ('user_email',)
