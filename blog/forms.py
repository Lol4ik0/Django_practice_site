from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from django.core.exceptions import ValidationError

from .models import *


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'blog/inc/custom_field.html'


class SendBackEmailForm(forms.Form):
    subject = forms.CharField(
        label='Тема',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'subject',
                'class': 'form-control',
                'placeholder': 'Your Subject',
            }
        )
    )
    message_content = forms.CharField(
        label='Текст листа',
        widget=forms.Textarea(
            attrs={
                'id': 'message_text',
                'class': 'textarea-message form-control',
                'placeholder': 'Your Message',
                'rows': '5'
            }
        )
    )
    user_name = forms.CharField(
        # label="Ваше ім'я",
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'name',
                'class': 'form-control',
                'placeholder': 'Your Name'
            }
        )
    )
    website = forms.CharField(
        # label='Ваш вебсайт',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'website',
                'class': 'form-control',
                'placeholder': 'Your Website'
            }
        )
    )
    email = forms.CharField(
        # label='Ваша пошта',
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'id': 'email',
                'class': 'form-control',
                'placeholder': 'Your-Email@gmail.com'
            }
        )
    )
    where_from = forms.CharField(
        # label='Звідки ви',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'address',
                'class': 'form-control',
                'placeholder': 'Where are You From?'
            }
        )
    )

    captcha = CaptchaField(
        widget=CustomCaptchaTextInput
    )
