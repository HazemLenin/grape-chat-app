from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

class AbstractModel(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class Profile(AbstractModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(_('birth date'))

    def __str__(self):
        return f'{self.user.username}\'s profile'


class Room(AbstractModel):
    title = models.CharField(max_length=265, unique=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='created_rooms')
    members = models.ManyToManyField(User, through='Membership', related_name='joined_rooms')

    def __str__(self):
        return self.title


class Membership(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} -> {self.room}'


class Message(AbstractModel):
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}\'s message'