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

class UserViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@gmail.com')
        self.client.force_authenticate(user=self.user)

    def test_list_with_query_param(self):
        url = reverse('api:user-list')
        query_param = {'search': 'test'}
        response = self.client.get(url, data=query_param, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_without_query_param(self):
        url = reverse('api:user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_valid_pk(self):
        user = User.objects.create_user(username='testuser2', password='testpassword', email='test2@gmail.com')
        url = reverse('api:user-detail', args=('1',))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)