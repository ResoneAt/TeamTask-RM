from django.urls import reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from api.views.accounts import SignUpAPIView

class SignUpAPIViewTest(APITestCase):

    def test_signup_valid_data(self):
        url = reverse('api:signup')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
    
    def test_signup_invalid_data(self):
        url = reverse('api:signup')
        data = {
            'username': '',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0) 
