from api.models import User
from rest_framework import serializers

from .models import (Company, PaidLeave, PaidLeaveDays, PaidLeaveRecord, User,
                     WorkRecord)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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


class PaidLeaveDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidLeaveDays
        fields = '__all__'
