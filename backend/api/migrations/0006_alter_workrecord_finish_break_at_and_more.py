# Generated by Django 4.0.4 on 2023-06-02 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_workrecord_work_contents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workrecord',
            name='finish_break_at',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workrecord',
            name='finish_overwork_at',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workrecord',
            name='finish_work_at',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workrecord',
            name='start_break_at',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workrecord',
            name='start_overwork_at',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workrecord',
            name='start_work_at',
            field=models.TimeField(blank=True, null=True),
        ),
    ]