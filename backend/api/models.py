from django.db import models


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=30)
    company_email = models.CharField(max_length=30)
    company_login_password = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company_name', 'company_email'], name='unique_company')
        ]


class User(models.Model):
    # Company削除時にUserも削除する
    company_id = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30)
    user_email = models.CharField(max_length=30)
    user_login_password = models.CharField(max_length=30)
    authority = models.CharField(max_length=10, choices=[('ADMIN', '管理者'), ('USER', '一般ユーザ')], default='user')
    commuting_expenses = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company_id', 'user_email'], name='unique_user')
        ]


class WorkRecord(models.Model):
    # User削除時にWorkRecordも削除する
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
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
    company_id = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
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
    company_id = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
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


class PaidLeaveDays(models.Model):
    company_id = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    year = models.IntegerField(unique=True)
    max_paid_leave_days = models.FloatField()
    used_paid_leave_days = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'year'], name='unique_paid_leave_days')
        ]
