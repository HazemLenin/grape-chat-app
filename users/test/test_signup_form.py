from django.test import TestCase
from users.forms import SignupForm


class TestSignupForm(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user123',
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'user@example.com',
            'password1': 'hello%world',
            'password2': 'hello%world'
        }

    def test_user_signup_form(self):
        data_copy = self.data.copy()

        # change username and email for uniqueness
        data_copy['username'] = 'newusername2'
        data_copy['email'] = 'new2@example.com'

        signup_form = SignupForm(data_copy)
        self.assertTrue(signup_form.is_valid())

    def test_user_signup_form_uniqueness(self):
        signup_form1 = SignupForm(self.data)
        self.assertTrue(signup_form1.is_valid())
        signup_form1.save()

        signup_form2 = SignupForm(self.data)
        self.assertFalse(signup_form2.is_valid())

    def test_user_signup_form_required_fields(self):
        data_copy = self.data.copy()

        del data_copy['username']
        del data_copy['email']
        del data_copy['password1']
        del data_copy['password2']

        signup_form = SignupForm(data_copy)
        self.assertFalse(signup_form.is_valid())

    def test_user_signup_form_password_validation(self):
        data_copy = self.data.copy()

        data_copy['password1'] = 'helloworld'
        data_copy['password2'] = 'helloworld'

        signup_form = SignupForm(data_copy)
        self.assertFalse(signup_form.is_valid())  # password validation error

    def test_user_signup_form_passwords_matching(self):
        data_copy = self.data.copy()

        data_copy['password1'] = 'hello%world'
        data_copy['password2'] = 'helloworld123'

        signup_form = SignupForm(data_copy)
        self.assertFalse(signup_form.is_valid())  # password matching error
