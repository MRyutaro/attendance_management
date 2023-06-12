from django.contrib import admin

from .models import (Company, PaidLeave, PaidLeaveDay, PaidLeaveRecord, User,
                     WorkRecord)

# TODO: adminにアクセスしたときにも同じsessionが使われるようにする
# from django.contrib.admin.sites import AdminSite


admin.site.register(User)
admin.site.register(Company)
admin.site.register(WorkRecord)
admin.site.register(PaidLeave)
admin.site.register(PaidLeaveRecord)
admin.site.register(PaidLeaveDay)