import profile
from django.contrib import admin
from core.models import Profile
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()

admin.site.register(User)
# admin.site.register(Profile)