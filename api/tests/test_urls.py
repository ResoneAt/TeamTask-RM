from django.test import TestCase
from django.urls import resolve, reverse
from api.views.card import MyCardsAPIView


class TestUrls(TestCase):
    def test_MyCardsAPIView(self):
        url = reverse('api:my-cards-list', args=('1',))
        self.assertEqual(resolve(url).func.view_class, MyCardsAPIView)