import re

from django.contrib.auth import authenticate
from django.forms import ModelForm, Form, CharField, PasswordInput, ValidationError

from apps.models import User


class RegisterForm(ModelForm):
    phone = CharField(max_length=20, required=True)
    password = CharField(widget=PasswordInput, required=True)
    confirm_password = CharField(widget=PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_phone(self):
        phone = self.data.get('phone')
        digits = re.sub(r'\D', '', phone)
        if not digits.startswith('998'):
            raise ValidationError("Telefon raqam 998 bilan boshlanishi kerak")
        if len(digits) != 12:
            raise ValidationError("Telefon raqam noto'g'ri kiritilgan")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(Form):
    phone = CharField()
    password = CharField()

    def clean_phone(self):
        phone = self.data.get('phone')
        return phone.removeprefix('+')

    def clean(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        self.user = authenticate(phone=phone, password=password)
        if not self.user:
            raise ValidationError("Invalid phone or password")
        return self.cleaned_data

    def get_user(self):
        return self.user
