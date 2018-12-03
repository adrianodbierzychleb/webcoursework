from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from match.models import Profile

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', "last_name", 'email']
