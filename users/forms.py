from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from django.core.exceptions import ValidationError

from .models import Users
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm



class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'users/custom_field.html'


class SendBackEmailForm(forms.Form):
    subject = forms.CharField(
        label='Тема',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    message_content = forms.CharField(
        label='Текст листа',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '5'
            }
        )
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput)

class UserRegisterForm(UserCreationForm):
    # groups = forms.ModelChoiceField(queryset=Group.objects.all())

    # my own fields visualisation in form settings
    username = forms.CharField(
        label='Username',
        min_length=5,
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    pib = forms.CharField(
        label='ПІБ',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    birth_date = forms.DateField(
        label='Дата народження',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'РРРР-ММ-ДД',
                # 'disabled': True
            }
        )
    )
    email = forms.EmailField(
        label='Пошта',
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'placeholder': 'name@example.com'
            }
        )
    )
    # photo = forms.ImageField(
    #     label='Фото',
    #     widget=forms.TextInput(
    #         attrs={
    #             'type': 'file',
    #             'class': 'form-control disable',
    #             # 'disabled': True
    #         }
    #     )
    # )
    phone = forms.CharField(
        label='Номер телефону',
        widget=forms.TextInput(
            attrs={
                # 'type': 'password',
                'class': 'form-control',
                'aria-describedby': "passwordHelpBlock",
                # 'disabled': True
            }
        )
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form'
            }
        )
    )
    password2 = forms.CharField(
        label='Підтвердження пароля',
        help_text='Введіть свій пароль ще раз',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form'
            }
        )
    )

    # Checking for occupied fields
    def clean_username(self):
        username = self.cleaned_data['username']
        if Users.objects.filter(username=username).exists():
            raise ValidationError("Користувач з таким ім'ям вже існує.")
        return username

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if Users.objects.filter(email=email).exists():
    #         raise ValidationError("На цій пошті вже є зареєстрований користувач.")
    #     return email

    # def clean_phone(self):
    #     phone = self.cleaned_data['phone']
    #     if Users.objects.filter(phone=phone).exists():
    #         raise ValidationError("На цьому номері вже є зареєстрований користувач.")
    #     return phone

    usable_password = None

    class Meta:
        model = Users
        # fields = '__all__
        fields = ('username', 'pib', 'birth_date', 'email', 'phone', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        min_length=5,
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form'
            }
        )
    )


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = Users
        # fields = '__all__
        fields = ('username', 'pib', 'photo')
