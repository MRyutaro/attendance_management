'''
ここに各エンドポイントに対するパーミッションを記述する
'''

from rest_framework.permissions import BasePermission


class IsLoggedInUser(BasePermission):
    def has_permission(self, request, view):
        # もしcookieにsession_idがあればTrueを返す
        if request.COOKIES.get('session_id'):
            return True
        else:
            return False
