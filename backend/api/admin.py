from django.contrib import admin

from .models import (Company, PaidLeave, PaidLeaveDays, PaidLeaveRecord, User,
                     WorkRecord)

admin.site.register(Company)
admin.site.register(User)
admin.site.register(WorkRecord)
admin.site.register(PaidLeave)
admin.site.register(PaidLeaveRecord)
admin.site.register(PaidLeaveDays)
