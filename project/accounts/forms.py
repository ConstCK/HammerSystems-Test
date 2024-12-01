from django import forms

from .models import Profile


class AuthForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)


class LoginForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('pass_code',)


class ActivateCodeForm(forms.Form):
    activated_code = forms.CharField(label='Активация invite кода')
