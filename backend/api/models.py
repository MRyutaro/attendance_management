from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
    # TODO: 会社には属してない人が見るページを作る
    """カスタムユーザーモデル"""
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": _("このメールアドレスは既に登録されています。"),
        },
    )
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text=_(
            "150字以下の半角英数字で入力してください。"
        ),
        validators=[username_validator],
    )
    # owner, manager, employeeの3種類
    role = models.CharField(
        max_length=10,
        choices=[
            ('owner', _('オーナー')),
            ('manager', _('マネージャー')),
            ('employee', _('従業員')),
        ],
        default='employee',
        help_text=_(
            'ユーザーの権限を設定します。\
            ownerは全ての権限を持ちます。\
            managerは従業員の管理ができます。\
            employeeは従業員の勤怠を入力できます。'
        ),
    )
    date_joined = None

    # emailアドレスをユーザー名として使用する
    USERNAME_FIELD = 'email'
    # ユーザー作成時に必要なフィールド
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("ユーザー")
        verbose_name_plural = _("ユーザー")
        # アプリ名_モデル名を動的に生成
        db_table = '{}_{}'.format('api', 'user')


class Company(TimeStampedModel, models.Model):
    email = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("会社")
        verbose_name_plural = _("会社")


class Belonging(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("所属")
        verbose_name_plural = _("所属")
        constraints = [
            models.UniqueConstraint(fields=['user', 'company'], name='unique_user_company')
        ]


# 誰が誰を招待したかを管理する
class Invitation(TimeStampedModel, models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_('招待した人'))
    # 招待された人のメールアドレス
    # TODO: これをもとに招待用のURLを作成する
    # TODO: 招待された人がもし会員登録していなかったら、会員登録画面に飛ばす
    invitee_email = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    token = models.CharField(max_length=30, unique=True)
    # tokenの有効期限は1日
    EXPIRIATION_DAYS = 1
    expiration_date = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=EXPIRIATION_DAYS),
        help_text=_('招待URLの有効期限です。デフォルトは1日です。')
    )

    class Meta:
        verbose_name = _("招待")
        verbose_name_plural = _("招待")
        # inviterのroleがownerかmanagerの時にinviteeを招待できる
        constraints = [
            models.CheckConstraint(
                check=models.Q(inviter__role='owner') | models.Q(inviter__role='manager'),
                name='check_inviter_role',
                violation_error_message=_('招待者の権限が不正です。')
            )
        ]


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
        verbose_name = _("勤怠記録")
        verbose_name_plural = _("勤怠記録")
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
        verbose_name = _("有給休暇")
        verbose_name_plural = _("有給休暇")
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
        verbose_name = _("有給休暇申請記録")
        verbose_name_plural = _("有給休暇申請記録")
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'paid_leave_date'],
                name='unique_paid_leave_record'
            )
        ]


class PaidLeaveDay(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    year = models.IntegerField(unique=True)
    max_paid_leave_days = models.FloatField()
    used_paid_leave_days = models.FloatField()

    class Meta:
        verbose_name = _("有給休暇日数")
        verbose_name_plural = _("有給休暇日数")
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'year'],
                name='unique_paid_leave_day'
            )
        ]
