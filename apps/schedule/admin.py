from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Group, UserName, ScheduleCondition

admin.site.register(Group)
admin.site.register(UserName)
admin.site.register(ScheduleCondition)
#admin.site.register(User)