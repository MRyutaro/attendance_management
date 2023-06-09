from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Company, PaidLeave, PaidLeaveDay, PaidLeaveRecord, WorkRecord
)
from django.contrib.auth import get_user_model

admin.site.register(Company)
admin.site.register(WorkRecord)
admin.site.register(PaidLeave)
admin.site.register(PaidLeaveRecord)
admin.site.register(PaidLeaveDay)

# AUTH_USER_MODELで指定したユーザーモデルを取得
User = get_user_model()

# https://zenn.dev/hathle/books/drf-auth-book/viewer/06_admin


class UserAdminCustom(UserAdmin):
    # ここで、/adminで表示する項目を設定する
    # 変えないとUserAdminのデフォルト項目になるのでエラーがでる。
    # ユーザー詳細
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'name',
                'password',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )
    list_display = ("name", "email", "is_staff", "is_superuser", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("name", "email")
    ordering = ("name", )


admin.site.register(User, UserAdminCustom)
