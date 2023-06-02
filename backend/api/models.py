from django.db import models

# Create your models here.


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=30)
    company_email = models.CharField(max_length=30, unique=True)
    company_login_password = models.CharField(max_length=30)


class User(models.Model):
    # Company削除時にUserも削除する
    company_id = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30)
    user_email = models.CharField(max_length=30, unique=True)
    user_login_password = models.CharField(max_length=30)
    authority = models.CharField(max_length=10, choices=[('ADMIN', '管理者'), ('USER', '一般ユーザ')], default='user')
    commuting_expenses = models.IntegerField(default=0)


class WorkRecord(models.Model):
    # User削除時にWorkRecordも削除する
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    # TODO: これだと1日に1人の従業員しか登録できないか確認する
    work_date = models.DateField(unique=True)
    start_work_at = models.TimeField()
    finish_work_at = models.TimeField()
    start_break_at = models.TimeField()
    finish_break_at = models.TimeField()
    start_overwork_at = models.TimeField()
    finish_overwork_at = models.TimeField()
    workplace = models.CharField(max_length=10, choices=[('OFFICE', 'オフィス'), ('HOME', '在宅'), ('OTHERS', 'その他')], default='OFFICE')
    work_contents = models.CharField(max_length=50, null=True, blank=True)


class PaidLeave(models.Model):
    company_id = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    work_type = models.CharField(
        max_length=20,
        choices=[
            ('WORKDAY', '平日'), ('DAY_OFF', '休日'), ('HOLIDAY', '祝日'), ('ALL_DAY_LEAVE', '全休'), ('MORNING_LEAVE', '午前休'), ('AFTERNOON_LEAVE', '午後休')
        ],
        default='WORKDAY'
    )


class PaidLeaveRecord(models.Model):
    paid_leave_record_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    paid_leave_date = models.DateField(unique=True)
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


class PaidLeaveDays(models.Model):
    company_id = models.ForeignKey(Company, db_column='company_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    year = models.IntegerField(unique=True)
    max_paid_leave_days = models.FloatField()
    used_paid_leave_days = models.FloatField()
