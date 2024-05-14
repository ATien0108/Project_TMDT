from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django import forms
from .models import *

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "Username", "class": "mt-10 form"})
        
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': "Email", "class": "mt-10 form"})
        
        self.fields['first_name'].widget = widgets.TextInput(
            attrs={'placeholder': "First Name", "class": "mt-10 form"})
        
        self.fields['last_name'].widget = widgets.TextInput(
            attrs={'placeholder': "Last Nname", "class": "mt-10 form"})
        
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'placeholder': "Password", "class": "mt-10 form"})
        
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'placeholder': "Repeat Password", "class": "mt-10 form"})

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("This email address is already exists.")
        return email

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name")
