from django import forms
from .models import UserName, ScheduleCondition
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
    class Meta:
        model = User
        fields = ('username', "password1", "password2",)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       #htmlの表示を変更可能にします
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = ScheduleCondition
        fields = ("month", "day", "place", "day_condition",)
        labels = {
            'month': '月',
            'day': '日',
            'time': '時間',
            'place': '場所',
            'day_condition': '日付',
        }
