 
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.all_rooms, name="all_rooms"),
    re_path(r'token$', views.token, name="token"),
    re_path(r'rooms/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),
]