from django import forms
from hcaptcha_field import hCaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                          'placeholder': 'username',
                                                                                          'autofocus': ''}))
    password = forms.CharField(label='password', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                          'placeholder': 'password'}))
    hcaptcha = hCaptchaField(label='captcha')


class RegisterForm(forms.Form):
    gender = (
        ('male', "Male"),
        ('female', "Female"),
    )
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="confirm password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='gender', choices=gender)
    hcaptcha = hCaptchaField(label='captcha')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()