from django.core.exceptions import ValidationError
from django.forms import widgets
from django import forms
from django.contrib.auth import get_user_model

class FormRegister(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=16,
        min_length=3,
        label='<i class="fa fa-user width-30" aria-hidden="true"></i>',
        error_messages={
            'required': '用户名不能为空',
            'min_length': "用户名最少3位",
            'max_length': "用户名最大16位"
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入账号'}),
    )
    password = forms.CharField(
        required=True,
        max_length=16,
        min_length=3,
        label='<i class="fa fa-unlock-alt width-30" aria-hidden="true"></i>',
        error_messages={
            'required': '密码不能为空',
            'min_length': "密码最少3位",
            'max_length': "密码最大16位"
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
    )
    re_password = forms.CharField(
        required=True,
        max_length=16,
        min_length=3,
        label='<i class="fa fa-lock width-30" aria-hidden="true"></i>',
        error_messages={
            'required': '确认密码不能为空',
            'min_length': "密码最少3位",
            'max_length': "密码最大16位"
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请确认密码'}),
    )
    email = forms.EmailField(
        required=True,
        label='<i class="fa fa-envelope width-30" aria-hidden="true"></i>',
        error_messages={
            'required': '邮箱不能为空'
        },
        widget=widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = get_user_model().objects.filter(username=username).exists()
        if user:
            raise ValidationError('该用户名已存在')
        else:
            return username

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')


class FormLogin(forms.Form):
    username = forms.CharField(
        required=True,
        label='<i class="fa fa-user width-30" aria-hidden="true"></i>',
        error_messages={
            'required': '用户名不能为空'
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入账号'}),
    )
    password = forms.CharField(
        required=True,
        label='<i class="fa fa-lock width-30" aria-hidden="true"></i>',
        error_messages={
            'required': '密码不能为空'
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
    )
