from django import forms
from .models import UserName, ScheduleCondition



class UserForm(forms.ModelForm):
    class Meta:
        model = UserName
        fields = ('user_name',)
        labels = {
            'user_name': 'ユーザー名',
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = ScheduleCondition
        fields = ('day_condition',)
        labels = {
            'day_condition': '日付',
        }