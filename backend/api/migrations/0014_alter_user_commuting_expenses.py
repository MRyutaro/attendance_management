# Generated by Django 4.0.4 on 2023-06-05 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_rename_company_id_paidleave_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='commuting_expenses',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
