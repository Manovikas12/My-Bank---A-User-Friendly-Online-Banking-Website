# forms.py
from django import forms
from django.core import validators


class LoginForm(forms.Form):
    client_id = forms.IntegerField(label="Account Number", error_messages={'required': 'Please enter your account number'})
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'required': 'Please enter your password'})
