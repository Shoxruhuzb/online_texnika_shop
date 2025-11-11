from django import forms
from django.contrib.auth import authenticate
from django.db.models.fields import CharField
from django.forms import ModelForm

from apps.models import User
from apps.serializers import UserPhoneSerializer


class RegisterForm(ModelForm):
    phone = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('phone',)  # ('phone', 'password', 'confirm_password') # """muammo bo'lsa"""

    def clean_phone(self):
        phone = self.data.get('phone')
        serializer = UserPhoneSerializer(data={'phone': phone})
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data['phone']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    phone = CharField()
    password = CharField()

    def clean(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        user = authenticate(username=phone, password=password)
        if not user:
            raise forms.ValidationError("Invalid phone or password")
        return self.cleaned_data
