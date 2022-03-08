from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from accounts.validators import validate_email
from accounts.models import Profile


class UserCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя', strip=False, required=False
    )
    email = forms.EmailField(
        label='email', required=True, validators=[validate_email, ]
    )

    password = forms.CharField(
        label='Пароль', strip=False, required=True,
        widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label='Подтвердить пароль', strip=False, required=True, widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password', 'Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'password', 'password_confirm', 'email'
        ]


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'about_profile', 'phone', 'gender']


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', ]


