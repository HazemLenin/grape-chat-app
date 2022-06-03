from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from core.models import Room, Membership

# Create your views here.

class RoomListView(generic.ListView):
    model = Room
    template_name = 'rooms/list.html'
    ordering = ['-id']
    paginate_by = 8


class RoomCreateView(SuccessMessageMixin, mixins.LoginRequiredMixin, generic.CreateView):
    model = Room
    fields = ('title',)
    template_name = 'rooms/new.html'
    success_message = 'Room successfully created!'

    def form_valid(self, form):
        form.instance.creator = self.request.user

        # this will set the self.object
        response =  super(RoomCreateView, self).form_valid(form)

        # Make creator membership
        Membership.objects.create(user=self.request.user, room=self.object, is_admin=True)

        return response

    def get_success_url(self):
        return reverse('rooms:room', kwargs={'pk': self.object.pk})


class RoomDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = Room
    template_name = 'rooms/detail.html'


class RoomUpdateView(SuccessMessageMixin, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.UpdateView):
    model = Room
    fields = ('title',)
    template_name = 'rooms/edit.html'
    success_message = 'Room updated successfully!'

    def test_func(self):
        return self.get_object().creator == self.request.user

    def get_success_url(self):
        return reverse('rooms:room', kwargs={'pk': self.object.pk})


class RoomDeleteView(SuccessMessageMixin, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView):
    model = Room
    template_name = 'delete.html'
    success_message = 'Room deleted successfully!'

    def test_func(self):
        return self.get_object().creator == self.request.user or self.request.user.is_admin

    def get_success_url(self):
        return reverse('rooms:rooms')