from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, user_email, password=None, *args, **kwargs):
        if not user_email:
            raise ValueError('이메일은 필수 입니다.')

        user = self.model(user_email=self.normalize_email(user_email), *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email, password, *args, **kwargs):
        user = self.create_user(user_email, password, *args, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None

    user_id = models.AutoField("유저 식별자", primary_key=True, db_column='유저id')
    user_email = models.EmailField("유저 이메일", max_length=100, unique=True, db_column='이메일')
    user_name = models.CharField("유저 이름", max_length=30, db_column='이름')
    user_nickname = models.CharField("유저 닉네임", max_length=20, unique=True, db_column='닉네임')
    user_phone = models.CharField("유저 전화번호", max_length=11,
                                  validators=[RegexValidator(regex=r'^\d+$', message="숫자만 입력하세요.")],
                                  null=False, blank=False, unique=True, db_column='전화번호')
    created_at = models.DateTimeField("생성 일시", auto_now_add=True, db_column='생성일시')

    objects = UserManager()

    # simpleJWT가 id를 찾을떄 user_id를 주도록 연결
    @property
    def id(self):
        return self.user_id

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_name'] #<- 배포 단계에서는 'user_nickname'을 다시 추가하고 하기

    class Meta:
        db_table = 'users'
