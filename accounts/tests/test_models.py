from django.test import TestCase
from accounts.models import User
from model_bakery import baker

class TestUserModel(TestCase):
    def test_model_str(self):
        user = baker.make(User, email='mojtaba@gmail.com')
        self.assertEqual(str(user), 'mojtaba@gmail.com')