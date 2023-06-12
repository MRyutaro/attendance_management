from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class TimeStampedModel(models.Model):
    """
    作成日時と更新日時を管理する抽象モデル
    他のモデルに継承させることで、作成日時と更新日時を自動的に管理することができる
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def _create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    # passwordは勝手にrequired=Trueになっているっぽい。
    def create_user(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, username, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    """カスタムユーザーモデル"""
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
    )
    date_joined = None

    # emailアドレスをユーザー名として使用する
    USERNAME_FIELD = 'email'
    # ユーザー作成時に必要なフィールド
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        # アプリ名_モデル名を動的に生成
        db_table = '{}_{}'.format('app', 'user')


class Company(TimeStampedModel, models.Model):
    email = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")


class WorkRecord(TimeStampedModel, models.Model):
    # on_delete=models.CASCADEでUser削除時にWorkRecordも削除する設定になってる
    # 多分userの中身はuser.idになってる
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_date = models.DateField()
    start_work_at = models.TimeField(null=True, blank=True)
    finish_work_at = models.TimeField(null=True, blank=True)
    start_break_at = models.TimeField(null=True, blank=True)
    finish_break_at = models.TimeField(null=True, blank=True)
    start_overwork_at = models.TimeField(null=True, blank=True)
    finish_overwork_at = models.TimeField(null=True, blank=True)
    workplace = models.CharField(
        max_length=10,
        choices=[
            ('office', _('オフィス')),
            ('home', _('在宅')),
            ('others', _('その他'))
        ],
        default='office'
    )
    work_contents = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'work_date'], name='unique_work_record')
        ]


class PaidLeave(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE)
    date = models.DateField()
    # TODO: 日付によって自動でdefaultを設定する
    work_type = models.CharField(
        max_length=20,
        choices=[
            ('workday', _('平日')),
            ('day_off', _('休日')),
            ('holiday', _('祝日')),
            ('all_day_leave', _('全休')),
            ('morning_leave', _('午前休')),
            ('afternoon_leave', _('午後休'))
        ],
        default='workday'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'date'], name='unique_paid_leave')
        ]


class PaidLeaveRecord(TimeStampedModel, models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    paid_leave_date = models.DateField()
    work_type = models.CharField(max_length=30)
    paid_leave_reason = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10,
        choices=[
            ('requested', _('リクエスト済み')),
            ('confirmed', _('承認済み')),
            ('rejected', _('拒否済み'))
        ],
        default='requested'
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    reject_reason = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'paid_leave_date'],
                name='unique_paid_leave_record'
            )
        ]


class PaidLeaveDay(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    year = models.IntegerField(unique=True)
    max_paid_leave_days = models.FloatField()
    used_paid_leave_days = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'year'],
                name='unique_paid_leave_day'
            )
        ]
