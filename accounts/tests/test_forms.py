from django.test import TestCase
from accounts.forms import UserRegistrationForm
from django.contrib.auth.models import User


class TestUserRegistrationForm(TestCase):
    def test_valid_data(self):
        form = UserRegistrationForm(data={'username':'moji', 'email':'moji@gmail.com', 'password1':'mojipass', 'password2':'mojipass'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),4)
    