from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from giveaid.models import User

class UserViewTests(APITestCase):

    def setUp(self):
        # Create a user for login tests
        unique_username = f'testuser_{uuid.uuid4()}'
        self.user = User.objects.create_user(
            username=unique_username,
            email=f'{unique_username}@example.com',
            password='testpassword'
        )

    # User Registration View Tests

    def test_user_registration_view(self):
        url = reverse('user_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'name': 'New User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(email='newuser@example.com').email, 'newuser@example.com')

    def test_user_registration_view_invalid_email(self):
        url = reverse('user_register')
        data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password': 'newpassword',
            'name': 'New User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_view_password_mismatch(self):
        url = reverse('user_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'wrongpassword',
            'name': 'New User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password2', response.data)

    def test_user_registration_view_short_password(self):
        url = reverse('user_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'short',
            'name': 'New User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_view_missing_name(self):
        url = reverse('user_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'name': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_user_registration_view_existing_email(self):
        url = reverse('user_register')
        data = {
            'username': 'newuser',
            'email': self.user.email,
            'password': 'newpassword',
            'name': 'New User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_view_existing_username(self):
        url = reverse('user_register')
        data = {
            'username': self.user.username,
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'name': 'New User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    # User Login View Tests

    def test_user_login_view(self):
        url = reverse('user_login')
        data = {
            'username': self.user.username,
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_view_invalid_credentials(self):
        url = reverse('user_login')
        data = {
            'username': 'wronguser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_user_login_view_incorrect_password(self):
        url = reverse('user_login')
        data = {
            'username': self.user.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_user_login_view_nonexistent_user(self):
        url = reverse('user_login')
        data = {
            'username': 'nonexistentuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_user_login_view_missing_password(self):
        url = reverse('user_login')
        data = {
            'username': self.user.username,
            'password': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_login_view_missing_username(self):
        url = reverse('user_login')
        data = {
            'username': '',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_user_login_view_with_whitespace_in_username(self):
        url = reverse('user_login')
        data = {
            'username': f' {self.user.username} ',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_view_with_trailing_spaces_in_password(self):
        url = reverse('user_login')
        data = {
            'username': self.user.username,
            'password': 'testpassword '
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_user_login_view_with_long_password(self):
        url = reverse('user_login')
        data = {
            'username': self.user.username,
            'password': 'a' * 256  # Assuming password should be less than or equal to 255 characters
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
