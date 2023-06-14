from django.core.mail import send_mail
from rest_framework import serializers
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import (
    User, Invitation, Belonging
)
from .exceptions import InvalidTokenError, ExpriedTokenError, UserDoesNotExistError, AlreadyBelongsError, InviterDoesNotBelongToAnyCompanyError

"""
データの中身をいじるクラス
- modelはモデルクラスを指定
- fieldsに与えるのはAPIとして出力したいフィールド名のタプル
"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # この値だけを使う？
        # TODO: これは何？データベースに保存する前のチェック？
        fields = ['email', 'password']
        # passwordは書き込みか更新しかしないようにする
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # ModelSerializerにはデフォルトで`create()` and `update()`が実装されている
        user = User.objects.create_user(**validated_data)
        return user


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['invitee_email', 'invitee_role']

    def create(self, validated_data):
        inviter = self.context['request'].user
        # inviterが所属しているcompanyを取得
        try:
            company = Belonging.objects.get(user=inviter).company
        except Belonging.DoesNotExist:
            raise InviterDoesNotBelongToAnyCompanyError(_('招待者は会社に所属していません。'))
        invitee_email = validated_data['invitee_email']
        invitee_role = validated_data.get('invitee_role', 'employee')
        token = get_random_string(length=30)
        invitation = Invitation.objects.create(
            inviter=inviter,
            invitee_email=invitee_email,
            invitee_role=invitee_role,
            company=company,
            token=token
        )

        # 招待メールの送信
        # 招待URLの作成->/compaies/<int:pk>/users/join/<str:token>の形式
        invitation_url = self.context['request'].build_absolute_uri(
            reverse('company_join', kwargs={'token': token})
        )

        # TODO: メールの内容を作成
        # subject = "会社への招待"
        # message = render_to_string(
        #     'invitation_email.html',
        #     context={
        #         'company': company,
        #         'invitation_url': invitation_url
        #     }
        # )
        # # settings.pyで設定したメールアドレスを使って送信
        # send_mail(subject, message, None, [invitee_email])

        return invitation


class JoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Belonging
        fields = []

    def create(self, validated_data):
        invitation = self.context['invitation']
        if not invitation:
            # raise serializers.ValidationError('Invitation does not exist')
            raise InvalidTokenError(_('招待トークンが無効です。'))
        elif invitation.expiration_time < timezone.now():
            # 新たにValueErrorを作成して返す
            # raise serializers.ValidationError('Invitation has expired')
            raise ExpriedTokenError(_('招待トークンの有効期限が切れています。'))

        # userが登録されていればそのユーザをbelongingに追加、いなければ新規登録画面に遷移するように指示する
        invitee_email = invitation.invitee_email
        user = User.objects.filter(email=invitee_email).first()
        if not user:
            # raise serializers.ValidationError('User does not exist')
            raise UserDoesNotExistError(_('ユーザが登録されていません。新規登録を行ってください。'))
        else:
            company = invitation.company
            if Belonging.objects.filter(user=user, company=company).exists():
                # raise serializers.ValidationError('User already belongs to the company')
                raise AlreadyBelongsError(_('ユーザは既にその会社に所属しています。'))
            else:
                invitation_role = invitation.invitee_role
                belonging = Belonging.objects.create(
                    user=user,
                    role=invitation_role,
                    company=company
                )
                return belonging
