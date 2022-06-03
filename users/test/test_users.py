from django.test import TestCase, Client
from django.urls import reverse, resolve
from users import views
from users.forms import SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUsers(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user123',
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'user@example.com',
            'password1': 'hello%world',
            'password2': 'hello%world'
        }

        for i in range(100):
            User.objects.create(username=f'username{i}', first_name='first_name', last_name='last_name', email=f'user{i}@email.com')
            
    def test_users_list(self):
        c = Client()
        response = c.get(reverse('users:users'))
        self.assertEqual(response.status_code, 200)
        
    def test_user_signup_and_user_detail_and_user_delete(self):
        c = Client()

        response = c.get(reverse('users:user-signup'))
        self.assertEqual(response.status_code, 200)

        response = c.post(reverse('users:user-signup'), self.data)
        self.assertEqual(response.status_code, 302)  # redirected

        # user detail
        response = c.get(reverse('users:user', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        # user delete
        response = c.post(reverse('users:user-delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)  # redirected

    def test_user_signup_form(self):
        signup_form = SignupForm(self.data)
        self.assertTrue(signup_form.is_valid())

    def test_user_signup_form_required_fields(self):
        dataCopy = self.data.copy()

        del dataCopy['username']
        del dataCopy['email']
        del dataCopy['password1']
        del dataCopy['password2']
        
        signup_form = SignupForm(dataCopy)
        self.assertFalse(signup_form.is_valid())  # password validation error

    def test_user_signup_form_password_validation(self):
        dataCopy = self.data.copy()

        dataCopy['password1'] = 'helloworld'
        dataCopy['password2'] = 'helloworld'
        
        signup_form = SignupForm(dataCopy)
        self.assertFalse(signup_form.is_valid())  # password validation error

    def test_user_signup_form_passwords_matching(self):
        dataCopy = self.data.copy()

        dataCopy['password1'] = 'hello%world'
        dataCopy['password2'] = 'helloworld123'
        
        signup_form = SignupForm(dataCopy)
        self.assertFalse(signup_form.is_valid())  # password matching error