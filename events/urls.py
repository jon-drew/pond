from django.conf.urls import url

from .views import EventCreateView, EventUpdateView, EventListView, EventDetailSlugView

urlpatterns = [
    url(r'^create/$', EventCreateView, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', EventDetailSlugView.as_view(), name='read'),
    url(r'^(?P<slug>[\w-]+)/update/$', EventUpdateView, name='update'),
    url(r'^$', EventListView.as_view(), name='list'),
]