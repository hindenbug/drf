from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from api.models import User, Team
import json

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

    def test_user_login(self):
        response = self.client.post('/login/', self.data, format='json')

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(self.user.token)

    def test_invalid_user_login(self):
        self.data = {'email': 'test_email@email.com', 'password': "password1"}
        response = self.client.post('/login/', self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(self.user.token)

    def test_team_creation_for_user_with_no_team(self):
        self.data = {'email': 'test_email@email.com', 'password': "password"}
        response = self.client.post('/login/', self.data, format='json')
        token = json.loads(response.content)['token']
        user = User.objects.get(email=self.data["email"])
        user.verified = True
        user.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/teams/', {"name": "Some Team"}, format='json')
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(user.team)

    def test_team_creation_for_user_with_a_team(self):
        self.data = {'email': 'test_email@email.com', 'password': "password"}
        response = self.client.post('/login/', self.data, format='json')
        token = json.loads(response.content)['token']
        user = User.objects.get(email=self.data["email"])
        user.verified = True
        user.team = Team.objects.create(name="Test Team")
        user.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/teams/', {"name": "Some Team"}, format='json')
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(user.team)
        self.assertEqual(user.team.name, "Test Team")

    def test_team_creation_for_user_with_no_team_without_passing_name(self):
        self.data = {'email': 'test_email@email.com', 'password': "password"}
        response = self.client.post('/login/', self.data, format='json')
        token = json.loads(response.content)['token']
        user = User.objects.get(email=self.data["email"])
        user.verified = True
        user.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/teams/', {}, format='json')
        user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(user.team)

    def test_invite_link_generation_for_user_with_no_team(self):
        self.data = {'email': 'test_email@email.com', 'password': "password"}
        response = self.client.post('/login/', self.data, format='json')
        token = json.loads(response.content)['token']
        user = User.objects.get(email=self.data["email"])
        user.verified = True
        user.save()
        user.refresh_from_db()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/invite/', {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invite_link_generation_for_user_with_no_team(self):
        self.data = {'email': 'test_email@email.com', 'password': "password"}
        response = self.client.post('/login/', self.data, format='json')
        token = json.loads(response.content)['token']
        user = User.objects.get(email=self.data["email"])
        user.verified = True
        user.save()
        user.refresh_from_db()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/invite/', {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
