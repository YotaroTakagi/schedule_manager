from django.contrib import admin


# Register your models here.
from .models import Group, UserName

admin.site.register(Group)
admin.site.register(UserName)
