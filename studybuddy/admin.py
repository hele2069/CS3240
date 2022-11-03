from django.contrib import admin
from .models import Profile, Courses, Schedule
from chat.models import Room

admin.site.register(Profile)

admin.site.register(Courses)

admin.site.register(Schedule)

# admin.site.register(Match)

admin.site.register(Room)