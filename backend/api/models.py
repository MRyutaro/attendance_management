from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.db import models


class Company(models.Model):
    # TODO: 会社を新規登録した日時を保存する
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=30)
    company_email = models.CharField(max_length=30, unique=True)
    company_login_password = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")

    def __str__(self):
        # pkを返す
        # 外部キーで呼び出すときとかはこれが呼ばれる
        # TODO: 自動でpkに設定されているから明記しなくてもいいかも
        return str(self.pk)


# class User(models.Model):
#     # Company削除時にUserも削除する設定になってる
#     company = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
#     user_id = models.AutoField(primary_key=True)
#     user_name = models.CharField(max_length=30)
#     user_email = models.CharField(max_length=30)
#     user_login_password = models.CharField(max_length=30)
#     authority = models.CharField(max_length=10, choices=[('ADMIN', '管理者'), ('USER', '一般ユーザ')], default='user')
#     # TODO: 0以上の整数にする
#     commuting_expenses = models.IntegerField(default=0, null=True, blank=True)
#     is_active = models.BooleanField(default=False)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['company_id', 'user_email'], name='unique_user')
#         ]


class CustomUserManager(BaseUserManager):
    def create_user(self, user_email, password, **extra_fields):
        if not user_email:
            raise ValueError('メールアドレスは必須です')

        user_email = self.normalize_email(user_email)
        user_email = user_email.lower()
        user = self.model(user_email=user_email, **extra_fields)
        user.set_password(password)
        user.save()
        # print(f"============user_email: {user_email}==============")
        # print(f"============password: {user.password}==============")
        return user

    # django\contrib\auth\management\commands\createsuperuser.py参照
    def create_superuser(self, user_email, password, **extra_fields):
        user = self.create_user(user_email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_email = models.EmailField(max_length=255, unique=True)
    user_name = models.CharField(max_length=255)
    # TODO: passwordがAbstractBaseUserで定義されている。その変数名だけを変更したい。

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    EMAIL_FIELD = "user_email"
    USERNAME_FIELD = 'user_email'

    def __str__(self):
        # pkを返す
        return str(self.pk)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


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
    workplace = models.CharField(max_length=10, choices=[('OFFICE', 'オフィス'), ('HOME', '在宅'), ('OTHERS', 'その他')], default='OFFICE')
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
    paid_leave_record_id = models.AutoField(primary_key=True)
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
