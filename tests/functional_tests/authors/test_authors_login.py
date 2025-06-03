from .base import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário ve o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Enter your username')
        password_field = self.get_by_placeholder(form, 'Enter your password')
        
        # Usuário preenche o formulário de login
        username_field.send_keys(user.username)
        password_field.send_keys('testpassword')

        #Usuário envia o formulário
        form.submit()

        # Usuário ve a mensagem de longin de sucesso
        self.assertIn(
            f'You are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_post(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )


    def test_form_login_is_invalid(self):
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário ve o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username = self.get_by_placeholder(form, 'Enter your username')
        password = self.get_by_placeholder(form, 'Enter your password')

        # Usuário preenche o formulário de login com dados inválidos
        username.send_keys(' ')
        password.send_keys(' ')

        # Usuário envia o formulário
        form.submit()

        # Usuário vê a mensagem de erro
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_invalid_credentials(self):
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário ve o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username = self.get_by_placeholder(form, 'Enter your username')
        password = self.get_by_placeholder(form, 'Enter your password')

        # Usuário preenche o formulário de login com dados que não existem
        username.send_keys('invaliduser')
        password.send_keys('invalidpassword')

        # Usuário envia o formulário
        form.submit()

        # Usuário vê a mensagem de erro
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
