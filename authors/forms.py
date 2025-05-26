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
        add_placeholder(self.fields['password'], 'Enter your password')
        add_placeholder(self.fields['password2'], 'Confirm your password')
    
    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must be 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        error_messages={
            'required': 'Username is required.',
            'min_length': 'Username must be at least 4 characters long.',
            'max_length': 'Username must be at most 150 characters long.',
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name.'},
        label='First Name',
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name.'},
        label='Last Name',
    )
    email = forms.EmailField(
        error_messages={'required': 'Email is required.'},
        label='E-mail Address',
        help_text='Please enter a valid email address.',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password is required.',
        },
        help_text=(
            'Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, and one number.'
        ),
        validators=[strong_password],
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password2',
        error_messages={
            'required': 'Please, repeat your password.',
        },
    )


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Passwords do not match.',
                'password2': 'Passwords do not match.'

            })