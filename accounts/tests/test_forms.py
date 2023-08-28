from django.test import TestCase
from accounts.forms import UserRegistrationForm
from accounts.models import User


class TestUserRegistrationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='moji', email='moji@gmail.com', password='mojipass')

    def test_valid_data(self):
        form = UserRegistrationForm(data={'username':'mojii', 'email':'mojii@gmail.com', 'password1':'mojipass', 'password2':'mojipass'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),4)
    
    def test_exist_email(self):
        form = UserRegistrationForm(data={'username':'nomoji', 'email': 'moji@gmail.com', 'password1':'moji', 'password2':'moji'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email'))

    def test_unmatched_passwords(self):
        form = UserRegistrationForm(data={'username':'moji', 'email':'moji@gmail.com', 'password1':'mojipasss', 'password2':'mojipas'})
        self.assertEqual(len(form.errors), 2)
        self.assertTrue(form.has_error)

