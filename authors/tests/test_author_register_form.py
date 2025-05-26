from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


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
        ('username', (
            'Username must be 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        )),
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

class AuthorRegisterFormIntegrationTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1', 
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'Username is required.'),
        ('first_name', 'Write your first name.'),
        ('last_name', 'Write your last name.'),
        ('password', 'Password is required.'),
        ('password2', 'Please, repeat your password.'),
        ('email', 'Email is required.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        #self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length(self):
        self.form_data['username'] = 'a'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must be at least 4 characters long.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must be at most 150 characters long.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, and one number.'
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))
        
        self.form_data['password'] = 'Str0ngP@ssword211'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')
        
        self.client.post(url, data=self.form_data, follow=True)
        
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'This email is already registered.'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'username': 'testuser',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        })

        self.client.post(url, data=self.form_data, follow=True)
        
        is_authenticated = self.client.login(
            username='testuser',
            password='Str0ngP@ssword1'
        )

        self.assertTrue(is_authenticated)