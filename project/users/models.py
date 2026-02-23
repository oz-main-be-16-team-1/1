from django.db import models

class User(models.Model):
    user_id = models.AutoField("유저 식별자", primary_key=True, db_column='유저id')
    user_email = models.EmailField("유저 이메일", max_length=100, db_column='이메일')
    user_name = models.CharField("유저 이름", max_length=30, db_column='이름')
    user_nickname = models.CharField("유저 닉네임", max_length=20, unique=True, db_column='닉네임')
    user_pw = models.CharField(max_length=255, db_column='패스워드')
    user_phone = models.CharField("유저 전화번호", max_length=15, unique=True, db_column='전화번호')
    recent_login = models.DateTimeField("최근 로그인 일시", null=True, db_column='최근 로그인')
    staff = models.BooleanField("스태프 여부", default=False, db_column='스태프여부')
    admin = models.BooleanField("관리자 여부", default=False, db_column='관리자여부')
    active = models.BooleanField("활성화 여부", default=True, db_column='활성화여부')
    created_at = models.DateTimeField("생성 일시", auto_now_add=True, db_column='생성일시')

    class Meta:
        db_table = 'users'