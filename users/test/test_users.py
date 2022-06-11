from django.test import TestCase, Client
from django.urls import reverse, resolve
from users import views
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

        data_copy = self.data.copy()

        data_copy['password'] = 'hello%world'

        del data_copy['password1']
        del data_copy['password2']

        User.objects.create(**data_copy)

    def test_users_list(self):
        c = Client()

        users_url = reverse('users:users')
        self.assertEqual(resolve(users_url).func.view_class, views.UserListView)

        response = c.get(users_url)
        self.assertEqual(response.status_code, 200)

    def test_user_signup(self):
        c = Client()
        data_copy = self.data.copy()

        # change username and email for uniqueness
        data_copy['username'] = 'newusername3'
        data_copy['email'] = 'new3@example.com'

        signup_url = reverse('users:user-signup')
        self.assertEqual(resolve(signup_url).func.view_class, views.UserSignupView)

        response = c.get(signup_url)
        self.assertEqual(response.status_code, 200)

        response = c.post(reverse('users:user-signup'), data_copy)
        self.assertEqual(response.status_code, 302)  # redirected

    def test_user_detail(self):
        # user detail
        user_url = reverse('users:user', kwargs={'pk': 1})
        self.assertEqual(resolve(user_url).func.view_class, views.UserDetailView)

        c = Client()
        response = c.get(user_url)
        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        # user delete
        delete_user_url = reverse('users:user-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(delete_user_url).func.view_class, views.UserDeleteView)

        c = Client()
        response = c.post(delete_user_url)
        self.assertEqual(response.status_code, 302)  # redirected
