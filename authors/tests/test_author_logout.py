from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertIn('Invalid credentials', response.content.decode('utf-8'))

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
        response = self.client.post(reverse('authors:logout'), data={'username': 'another_user'}, follow=True)
        self.assertIn('Invalid logout user', response.content.decode('utf-8'))

    def test_user_can_logout_sucessfully(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
        response = self.client.post(reverse('authors:logout'), data={'username': 'testuser'}, follow=True)
        self.assertIn('Logged out successfully', response.content.decode('utf-8'))
    

        
    