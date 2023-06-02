# Generated by Django 4.0.4 on 2023-06-02 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=30)),
                ('company_email', models.CharField(max_length=30, unique=True)),
                ('company_login_password', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='authority',
            field=models.CharField(choices=[('ADMIN', '管理者'), ('USER', '一般ユーザ')], default='user', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='commuting_expenses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='user_email',
            field=models.CharField(default='a@a.com', max_length=30, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='user_login_password',
            field=models.CharField(default=1028, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(default='admin', max_length=30),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='WorkRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.DateField(unique=True)),
                ('start_work_at', models.TimeField()),
                ('finish_work_at', models.TimeField()),
                ('start_break_at', models.TimeField()),
                ('finish_break_at', models.TimeField()),
                ('start_overwork_at', models.TimeField()),
                ('finish_overwork_at', models.TimeField()),
                ('workplace', models.CharField(choices=[('OFFICE', 'オフィス'), ('HOME', '在宅'), ('OTHERS', 'その他')], default='OFFICE', max_length=10)),
                ('work_contents', models.CharField(max_length=50)),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='PaidLeaveRecord',
            fields=[
                ('paid_leave_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('paid_leave_date', models.DateField(unique=True)),
                ('work_type', models.CharField(max_length=30)),
                ('paid_leave_reason', models.CharField(max_length=50)),
                ('requested_at', models.DateTimeField()),
                ('status', models.CharField(choices=[('REQUESTED', 'リクエスト済み'), ('CONFIRMED', '承認済み'), ('REJECTED', '拒否済み')], default='REQUESTED', max_length=10)),
                ('confirmed_at', models.DateTimeField(blank=True, null=True)),
                ('reject_reason', models.CharField(blank=True, max_length=50, null=True)),
                ('company_id', models.ForeignKey(db_column='company_id', on_delete=django.db.models.deletion.CASCADE, to='api.company')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='PaidLeaveDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
                ('max_paid_leave_days', models.FloatField()),
                ('used_paid_leave_days', models.FloatField()),
                ('company_id', models.ForeignKey(db_column='company_id', on_delete=django.db.models.deletion.CASCADE, to='api.company')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='PaidLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('work_type', models.CharField(choices=[('WORKDAY', '平日'), ('DAY_OFF', '休日'), ('HOLIDAY', '祝日'), ('ALL_DAY_LEAVE', '全休'), ('MORNING_LEAVE', '午前休'), ('AFTERNOON_LEAVE', '午後休')], default='WORKDAY', max_length=20)),
                ('company_id', models.ForeignKey(db_column='company_id', on_delete=django.db.models.deletion.CASCADE, to='api.company')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='company_id',
            field=models.ForeignKey(db_column='company_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='api.company'),
            preserve_default=False,
        ),
    ]
