from django.conf.urls import url

from .views import RibbitCreateView, RibbitUpdateView, RibbitListView, RibbitDetailSlugView

urlpatterns = [
    url(r'^create/$', RibbitCreateView, name='create'),
    url(r'^(?P<slug>[\w-]+)/update/$', RibbitUpdateView, name='update'),
    url(r'^(?P<slug>[\w-]+)/$', RibbitDetailSlugView.as_view(), name='read'),
    url(r'^$', RibbitListView.as_view(), name='list'),
]