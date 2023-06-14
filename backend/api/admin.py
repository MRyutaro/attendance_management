from django.contrib import admin

from .models import (Belonging, Company, Invitation, PaidLeave, PaidLeaveDay,
                     PaidLeaveRecord, User, WorkRecord, Role)


admin.site.register(User)
admin.site.register(Company)
admin.site.register(WorkRecord)
admin.site.register(PaidLeave)
admin.site.register(PaidLeaveRecord)
admin.site.register(PaidLeaveDay)
admin.site.register(Belonging)
admin.site.register(Invitation)
admin.site.register(Role)
