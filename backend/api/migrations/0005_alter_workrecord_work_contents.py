# Generated by Django 4.0.4 on 2023-06-02 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_company_remove_user_created_at_remove_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workrecord',
            name='work_contents',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]