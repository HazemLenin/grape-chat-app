from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from .forms import SignupForm, ProfileForm, UserUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth import mixins

# Create your views here.

User = get_user_model()

class SignupView(SuccessMessageMixin, generic.CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_message = 'Thank you for registering!'

    def get_success_url(self):
        return reverse('core:home')


class UserListView(generic.ListView):
    model = User
    template_name = 'users/list.html'
    ordering = ['-id']
    paginate_by = 8


class UserDetailView(generic.DetailView):
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'object'


class UserUpdateView(SuccessMessageMixin, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/edit.html'
    success_message = 'Profile updated successfully!'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse('users:user', kwargs={'pk': self.request.user.pk})


class UserDeleteView(SuccessMessageMixin, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView):
    model = User
    template_name = 'delete.html'
    success_message = 'Profile deleted successfully!'

    def test_func(self):
        return self.get_object() == self.request.user or self.request.user.is_admin

    def get_success_url(self):
        return reverse('users:users')
