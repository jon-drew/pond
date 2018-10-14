"""pond URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import TemplateView, CreateView

urlpatterns = [
    url(r'^$', auth_views.LoginView.as_view(), name='login'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url('^register/', CreateView.as_view(
            template_name='registration/register.html',
            form_class=UserCreationForm,
            success_url='/'
    ), name='register'),
    url(r'^hoppers/', include(('hoppers.urls', 'hoppers'), namespace='hopppers')),
    url(r'^pads/', include(('pads.urls', 'pads'), namespace='pads')),
    url(r'^events/', include(('events.urls', 'events'), namespace='events')),
    url(r'^ribbits/', include(('ribbits.urls', 'ribbits'), namespace='ribbits')),
]
