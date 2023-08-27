from django.test import TestCase
from django.urls import resolve, reverse
from api.views.card import MyCardsAPIView, CardAPIView, CardCreateAPIView, CardUpdateAPIView, \
                        CardDeleteAPIView


class TestUrls(TestCase):
    def test_MyCardsAPIView(self):
        url = reverse('api:my-cards-list', args=('1',))
        self.assertEqual(resolve(url).func.view_class, MyCardsAPIView)

    def test_CardAPIView(self):
        url = reverse('api:card-detail', args=('1',))
        self.assertEqual(resolve(url).func.view_class, CardAPIView)

    def test_CardCreateAPIView(self):
        url = reverse('api:create-card', args=('1',))
        self.assertEqual(resolve(url).func.view_class, CardCreateAPIView)

    def test_CardUpdateAPIView(self):
        url = reverse('api:update-card', args=('1',))
        self.assertEqual(resolve(url).func.view_class, CardUpdateAPIView)

    def test_CardDeleteAPIView(self):
        url = reverse('api:delete-card', args=('1',))
        self.assertEqual(resolve(url).func.view_class, CardDeleteAPIView)
        