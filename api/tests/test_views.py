from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from api.models import User

class ApiViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.data = {'email': 'test_email@email.com', 'password': "password"}
        response = self.client.post('/register/', self.data, format='json')
        self.user = User.objects.get(email=self.data["email"])

    def test_register_new_user(self):
        self.data = { "email": "test_email_new@gmail.com", "first_name": "Test", "last_name": "Lastname", "password": "12345678" }
        response = self.client.post('/register/', self.data, format='json')
        new_user = User.objects.get(email=self.data["email"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertFalse(self.user.verified)
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

    def test_verify_new_user(self):
        response = self.client.post("/verify/" + str(self.user.verification_key) + "/" , format='json')

        self.user.refresh_from_db()
        self.assertTrue(self.user.verified)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_verify_new_user_with_wrong_verification_key(self):
        response = self.client.post("/verify/sbc21f34b098265c4723b38315c471c2/", format='json')

        self.assertFalse(self.user.verified)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_do_not_verify_new_user_with_invalid_verification_key_length(self):
        response = self.client.post("/verify/somerandomekey/", format='json')

        self.assertFalse(self.user.verified)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_do_not_verify_user_already_verified(self):
        self.user.verified = True
        self.user.save()
        self.user.refresh_from_db()
        response = self.client.post("/verify/" + str(self.user.verification_key) + "/" , format='json')

        self.assertTrue(self.user.verified)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
