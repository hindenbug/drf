from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from api.models import User

class ApiViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.data = {'email': 'test_email@email.com', 'password': "password"}
        self.client.post('/register/', self.data, format='json')

    def test_register_new_user(self):
        self.data = { "email": "test_email_new@gmail.com", "first_name": "Test", "last_name": "Lastname", "password": "12345678" }
        response = self.client.post('/register/', self.data, format='json')
        new_user = User.objects.get(email=self.data["email"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertIsNotNone(new_user.verification_key)

    def test_to_not_register_new_user_without_password(self):
        self.data = { "email": "test_email_new@gmail.com", "first_name": "Test", "last_name": "Lastname" }
        response = self.client.post('/register/', self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_to_not_register_existing_user(self):
        response = self.client.post('/register/', self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
