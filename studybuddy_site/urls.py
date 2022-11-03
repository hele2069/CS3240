"""studybuddy_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views
from studybuddy.views import CustomLoginView
from studybuddy.forms import LoginForm
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('google', TemplateView.as_view(template_name="index.html")),
    # path('', TemplateView.as_view(template_name="homepage.html")),
    path('', include('studybuddy.urls')),
    # path('register/', TemplateView.as_view(template_name="studybuddy/register.html")),
    # path('accounts/', include('allauth.urls')),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='studybuddy/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='studybuddy/logout.html'), name='logout'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    re_path('rooms', include('chat.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


