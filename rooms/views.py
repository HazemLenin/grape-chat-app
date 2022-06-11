from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from core.models import Room, Membership
from django.contrib import messages

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

        return super(RoomCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('rooms:room', kwargs={'pk': self.object.pk})


class RoomDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = Room
    template_name = 'rooms/detail2.html'


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


def room_join(request, pk):
    room = get_object_or_404(Room, pk=pk)
    # try:
    #     Membership.objects.get(user=request.user, room=room)
    #     messages.error(request, 'You already a member of this room!')
    # except Membership.DoesNotExist:
    #     Membership.objects.create(user=request.user, room=room)
    #     messages.success(request, 'You joined the room!')

    if request.user in room.members.all():
        messages.error(request, 'You already a member of this room!')

    else:
        room.members.add(request.user)
        messages.success(request, 'You joined the room successfully!')

    return redirect(reverse('rooms:room', kwargs={"pk": room.pk}))