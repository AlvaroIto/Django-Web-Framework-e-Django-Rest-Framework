from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Enter your first name'),
        ('last_name', 'Enter your last name'),
        ('username', 'Enter your username'),
        ('email', 'Enter your email address'),
        ('password', 'Enter your password'),
        ('password2', 'Confirm your password')
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)
 
    @parameterized.expand([
        ('username', 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        ('email', 'Please enter a valid email address.'),
        ('password', (
            'Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, and one number.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)
        
    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'E-mail Address'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)
