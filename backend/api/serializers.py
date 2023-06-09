from rest_framework import serializers

from .models import (
    Company, PaidLeave, PaidLeaveDay, PaidLeaveRecord, CustomUser, WorkRecord
)

"""
Models.pyで定義したモデルをJSON形式に変換するためのクラス
"""


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # この値だけを使う？
        fields = ['id', 'company', 'email', 'password']

        # こんな感じで、このクラスでバリデーションを行う。
        # 参考 -> https://leben.mobi/blog/django_rest_flamework_api/python/
        # def validate_username(self, username):
        #     if 'hoge' in username.lower():
        #         raise serializers.ValidationError('The username `hoge` can not be used.')
        #     return username
        # def validate(self, data):
        #     if 'hoge' in data['first_name'].lower() and 'fuga' in data['last_name'].lower():
        #         raise serializers.ValidationError('The first name `hoge` and last name `fuga` can not be used.')
        #     return data


class WorkRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkRecord
        fields = '__all__'


class PaidLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidLeave
        fields = '__all__'


class PaidLeaveRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidLeaveRecord
        fields = '__all__'


class PaidLeaveDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidLeaveDay
        fields = '__all__'
