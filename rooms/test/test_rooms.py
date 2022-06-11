from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rooms import views

User = get_user_model()


class TestRooms(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user123',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'user@example.com',
            'password': 'hello%world'
        }
        User.objects.create(**self.data)

    def test_rooms_list(self):
        c = Client

        rooms_url = reverse('rooms:rooms')
        self.assertEqual(resolve(rooms_url).func.view_class, views.RoomListView)

    def test_room_detail(self):
        room_url = reverse('rooms:room', kwargs={'pk': 1})
        self.assertEqual(resolve(room_url).func.view_class, views.RoomDetailView)

    def test_room_create(self):
        room_create_url = reverse('rooms:room-new')
        self.assertEqual(resolve(room_create_url).func.view_class, views.RoomCreateView)

    def test_room_edit(self):
        room_edit_url = reverse('rooms:room-edit', kwargs={'pk': 1})
        self.assertEqual(resolve(room_edit_url).func.view_class, views.RoomUpdateView)

    def test_room_delete(self):
        room_delete_url = reverse('rooms:room-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(room_delete_url).func.view_class, views.RoomDeleteView)

    def test_room_join(self):
        room_join_url = reverse('rooms:room-join', kwargs={'pk': 1})
        self.assertEqual(resolve(room_join_url).func, views.room_join)