import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from giveaid.models import User

class UserAPITests(APITestCase):

    def setUp(self):
        User.objects.all().delete()
        unique_username = f'testuser_{uuid.uuid4()}'
        self.user = User.objects.create_user(
            username=unique_username,
            email=f'{unique_username}@example.com',
            password='testpassword'
        )

    # User Registration Tests

    def test_user_registration(self):
        url = reverse('user_register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'name': 'New User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(email='newuser@example.com').email, 'newuser@example.com')

    def test_user_registration_invalid_data(self):
        url = reverse('user_register')
        data = {
            'email': '',
            'password': 'testpassword',
            'name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_invalid_email(self):
        url = reverse('user_register')
        data = {
            'email': 'invalid-email',
            'password': 'testpassword',
            'name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_missing_password(self):
        url = reverse('user_register')
        data = {
            'email': 'testuser@example.com',
            'password': '',
            'name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_existing_email(self):
        url = reverse('user_register')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'name': 'Another User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_missing_name(self):
        url = reverse('user_register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'name': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_user_registration_short_password(self):
        url = reverse('user_register')
        data = {
            'email': 'shortpassword@example.com',
            'password': 'short',
            'name': 'Short Password User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_long_name(self):
        url = reverse('user_register')
        data = {
            'email': 'longname@example.com',
            'password': 'validpassword',
            'name': 'A' * 101  # Assuming name should be less than or equal to 100 characters
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_user_registration_with_invalid_password(self):
        url = reverse('user_register')
        data = {
            'email': 'invalidpassword@example.com',
            'password': '123',  # Password less than 8 characters
            'name': 'Invalid Password User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    # User Login Tests

    def test_user_login(self):
        url = reverse('user_login')
        data = {
            'email': self.user.email,
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User Logged in successfully')

    def test_user_login_fail(self):
        url = reverse('user_login')
        data = {
            'email': 'wronguser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Incorrect credentials')

    def test_user_login_incorrect_password(self):
        url = reverse('user_login')
        data = {
            'email': self.user.email,
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Incorrect credentials')

    def test_user_login_nonexistent_user(self):
        url = reverse('user_login')
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'User Not Found')

    def test_user_login_missing_password(self):
        url = reverse('user_login')
        data = {
            'email': self.user.email,
            'password': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_login_missing_email(self):
        url = reverse('user_login')
        data = {
            'email': '',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_login_with_whitespace_in_email(self):
        url = reverse('user_login')
        data = {
            'email': f' {self.user.email} ',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User Logged in successfully')

    def test_user_login_with_special_characters_in_password(self):
        url = reverse('user_login')
        data = {
            'email': self.user.email,
            'password': 'p@ssw0rd!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Incorrect credentials')

    def test_user_login_with_trailing_spaces_in_password(self):
        url = reverse('user_login')
        data = {
            'email': self.user.email,
            'password': 'testpassword '
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Incorrect credentials')

    def test_user_login_with_long_password(self):
        url = reverse('user_login')
        data = {
            'email': self.user.email,
            'password': 'a' * 256  # Assuming password should be less than or equal to 255 characters
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Incorrect credentials')

    # User Model Tests

    def test_user_required_fields(self):
        unique_username = f'requiredfields_{uuid.uuid4()}'
        user = User.objects.create_user(
            username=unique_username,
            email=f'{unique_username}@example.com',
            password='testpassword'
        )
        self.assertEqual(user.username, unique_username)
        self.assertEqual(user.email, f'{unique_username}@example.com')
