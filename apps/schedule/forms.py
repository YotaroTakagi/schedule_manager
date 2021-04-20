from django import forms
from .models import UserName



class UserForm(forms.ModelForm):
    class Meta:
        model = UserName
        fields = ('user_name',)
        labels = {
            'user_name': 'ユ,ーザー名',
        }