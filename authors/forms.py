from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail Address',
            'password': 'Password'
        }
        help_texts = {
            'email': 'Please enter a valid email address.',
        }
        error_messages = {
            'username': {
                'required': 'Username is required.',
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name',
                'class': 'input text-input outra-classe'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Enter your password',
            })
            
        }