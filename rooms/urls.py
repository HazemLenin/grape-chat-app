from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.RoomListView.as_view(), name='rooms'),
    path('new/', views.RoomCreateView.as_view(), name='room-new'),
    path('<int:pk>/', views.RoomDetailView.as_view(), name='room'),
    path('<int:pk>/edit/', views.RoomUpdateView.as_view(), name='room-edit'),
    path('<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room-delete'),
    path('<int:pk>/join/', views.room_join, name='room-join'),
]