from django.conf.urls import url

from .views import EventCreateView, EventDetailSlugView, EventUpdateView, EventListView

from ribbits.views import RibbitEventCreateView

urlpatterns = [
    url(r'^create/$', EventCreateView, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', EventDetailSlugView.as_view(), name='read'),
    url(r'^(?P<slug>[\w-]+)/update/$', EventUpdateView, name='update'),
    url(r'^$', EventListView.as_view(), name='list'),

    # Create a ribbit from an event
    url(r'^(?P<event>[\w-]+)/create/$', RibbitEventCreateView, name='create_ribbit'),
]