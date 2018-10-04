from django.conf.urls import url

from .views import HopperListView, HopperDetailSlugView, ListenerCreateView

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', HopperDetailSlugView.as_view(), name='read'),
    url(r'^$', HopperListView.as_view(), name='list'),
    url(r'^create/$', ListenerCreateView, name='create'),
]