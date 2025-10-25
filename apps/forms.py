from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models.fields import CharField
from django.forms import ModelForm

from apps.models import User


class RegisterForm(ModelForm):
    phone = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('phone',)   # ('phone', 'password', 'confirm_password') # """muammo bo'lsa"""

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
        user = authenticate(phone=phone, password=password)
        if not user:
            raise forms.ValidationError("Invalid phone or password")
        return self.cleaned_data

    # email = EmailField(
    #     max_length=254,
    #     help_text='Required. Please enter a valid email address.',
    #     error_messages={}
    # )
    # identifier = CharField(
    #     label="Email yoki telefon raqam (+998)",
    #     max_length=100,
    #     required=True,
    # )
    #
    # class Meta:
    #     model = User
    #     fields = ('identifier', 'password1', 'password2')
    #
    #
    # def validate_phone_number(self, value):
    #     digits_only = ''.join(re.findall(r'\d', value))
    #     if len(digits_only) != 9:
    #         raise forms.ValidationError("Telefon raqam 9 ta raqamdan iborat bo'lishi kerak.")
    #     return digits_only
    #
    # def clean_identifier(self):
    #     identifier = self.cleaned_data.get('identifier')
    #
    #     if not identifier:
    #         raise forms.ValidationError("Iltimos, email yoki telefon raqam kiriting.")
    #
    #     if '@' in identifier:
    #         if not forms.EmailField().clean(identifier):
    #             raise forms.ValidationError("Email noto'g'ri formatda.")
    #     else:
    #         digits_only = ''.join(re.findall(r'\d', identifier))
    #         if len(digits_only) != 9:
    #             raise forms.ValidationError("Telefon raqam 9 ta raqamdan iborat bo'lishi kerak.")
    #     return identifier
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     identifier = cleaned_data.get('identifier')
    #
    #     if User.objects.filter(username=identifier).exists():
    #         raise forms.ValidationError("Bu email yoki telefon raqam allaqachon ro'yxatdan o'tgan.")
    #
    #     return cleaned_data
    #
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     identifier = self.cleaned_data.get('identifier')
    #
    #     user.username = identifier
    #     if '@' in identifier:
    #         user.email = identifier
    #         user.phone = ''
    #     else:
    #         user.phone = identifier
    #         user.email = ''
    #
    #     if commit:
    #         user.save()
    #     return user