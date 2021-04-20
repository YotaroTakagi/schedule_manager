from django.contrib import admin


# Register your models here.
from .models import Group, UserName, ScheduleCondition

admin.site.register(Group)
admin.site.register(UserName)
admin.site.register(ScheduleCondition)
