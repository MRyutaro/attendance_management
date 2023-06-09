from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class Company(models.Model):
    email = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, company, email, password, **extra_fields):
        if not company:
            raise ValueError(_('会社idは必須です。'))
        if not email:
            raise ValueError(_('メールアドレスは必須です。'))
        if not password:
            raise ValueError(_('パスワードは必須です。'))
        email = self.normalize_email(email)
        user = self.model(company=company, email=email, **extra_fields)
        user.set_password(password)
        try:
            user.save(using=self.db)
        except Exception as e:
            raise ValueError(f"Failed to save user: {e}")

        return user

    def create_user(self, company, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(company, email, password, **extra_fields)

    def create_superuser(self, company, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('authority', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('スーパーユーザーはis_staff=Trueでなければなりません。'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('スーパーユーザーはis_superuser=Trueでなければなりません。'))
        if extra_fields.get('authority') != 'ADMIN':
            raise ValueError(_('スーパーユーザーはauthority=ADMINでなければなりません。'))

        return self._create_user(company, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    authority = models.CharField(
        max_length=10, choices=[('ADMIN', '管理者'), ('USER', '一般ユーザ')], default='USER'
    )
    commuting_expenses = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # カスタマイズしたモデルのCRUDのために必要. objects.create_user()などを使えるようになる
    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'


class WorkRecord(models.Model):
    # User削除時にWorkRecordも削除する設定になってる
    user = models.ForeignKey(CustomUser, db_column='user_id', on_delete=models.CASCADE)
    work_date = models.DateField()
    start_work_at = models.TimeField(null=True, blank=True)
    finish_work_at = models.TimeField(null=True, blank=True)
    start_break_at = models.TimeField(null=True, blank=True)
    finish_break_at = models.TimeField(null=True, blank=True)
    start_overwork_at = models.TimeField(null=True, blank=True)
    finish_overwork_at = models.TimeField(null=True, blank=True)
    workplace = models.CharField(
        max_length=10, choices=[('OFFICE', 'オフィス'), ('HOME', '在宅'), ('OTHERS', 'その他')], default='OFFICE'
    )
    work_contents = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'work_date'], name='unique_work_record')
        ]


class PaidLeave(models.Model):
    company = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, db_column='user_id', on_delete=models.CASCADE)
    date = models.DateField()
    work_type = models.CharField(
        max_length=20,
        choices=[
            ('WORKDAY', '平日'), ('DAY_OFF', '休日'), ('HOLIDAY', '祝日'), ('ALL_DAY_LEAVE', '全休'), ('MORNING_LEAVE', '午前休'), ('AFTERNOON_LEAVE', '午後休')
        ],
        default='WORKDAY'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'date'], name='unique_paid_leave')
        ]


class PaidLeaveRecord(models.Model):
    company = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, db_column='user_id', on_delete=models.CASCADE)
    paid_leave_date = models.DateField()
    work_type = models.CharField(max_length=30)
    paid_leave_reason = models.CharField(max_length=50)
    requested_at = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=[('REQUESTED', 'リクエスト済み'), ('CONFIRMED', '承認済み'), ('REJECTED', '拒否済み')],
        default='REQUESTED'
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    reject_reason = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'paid_leave_date', 'status'], name='unique_paid_leave_record')
        ]


class PaidLeaveDay(models.Model):
    company = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, db_column='user_id', on_delete=models.CASCADE)
    year = models.IntegerField(unique=True)
    max_paid_leave_days = models.FloatField()
    used_paid_leave_days = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'year'], name='unique_paid_leave_days')
        ]
