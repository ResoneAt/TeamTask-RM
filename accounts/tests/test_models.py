from django.test import TestCase
from accounts.models import User
from model_bakery import baker

class TestUserModel(TestCase):
    def setUp(self):
        self.user = baker.make(User, email='mojtaba@gmail.com')

    def test_model_str(self):
        self.assertEqual(str(self.user), 'mojtaba@gmail.com')