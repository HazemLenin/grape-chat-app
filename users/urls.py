from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('signup/', views.SignupView.as_view(), name='user-signup'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user'),
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='user-edit'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
]
