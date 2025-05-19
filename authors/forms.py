from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    regex = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, and one number.'
        ), 
            code='invalid'
        )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Enter your first name')
        add_placeholder(self.fields['last_name'], 'Enter your last name')
        add_placeholder(self.fields['username'], 'Enter your username')
        add_placeholder(self.fields['email'], 'Enter your email address')
    

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
        }),
        error_messages={
            'required': 'Password is required.',
        },
        help_text=('Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, and one number.'),
        validators=[strong_password]
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
        })
    )


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

    def clean_password(self):
        data = self.cleaned_data.get('password')
        
        return data
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Passwords do not match.',
                'password2': 'Passwords do not match.'

            })