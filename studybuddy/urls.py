from django.urls import path, include, re_path
from django.contrib import admin
from .views import about, homepage, RegisterView, profile, change_password, course_list
from django.urls import path, include
from .views import homepage, RegisterView, profile, change_password, course_list, search_courses, my_courses, add_remove_courses, start_matching, get_matches, schedule_class, schedule_view, schedule, match_room
from django.contrib.auth import views as authviews
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', homepage, name='homepage'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('password/', change_password, name='change_password'),
    path('courses/', course_list, name='course_list'),
    path('my_courses/', my_courses, name='my_courses'),
    path('my_courses/search_results', search_courses, name='search_courses'),
    path('my_courses/search_results/add_courses', add_remove_courses, name='add_courses'),
    path('my_courses/search_results/remove_courses', add_remove_courses, name='remove_courses'),
    re_path('rooms', include('chat.urls')),
    re_path(r'^', include('chat.urls')),
    path('search_courses/', search_courses, name='search_courses'),
    path('start_matching/', start_matching, name='start_matching'),
    path('get_matches/', get_matches, name='get_matches'),
    path('get_matches/match/', match_room, name='match_room'),
    path('about/', about, name='about'),
    path('schedule_meeting/', schedule_view, name='schedule_view'),
    path('schedule_class/', schedule_class, name='schedule_class'),
    path('schedule/', schedule, name='schedule'),
    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catalog'),

]

