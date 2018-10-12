from django.conf.urls import url

from .views import RibbitCreateView, RibbitListView, RibbitDetailSlugView

urlpatterns = [
    url(r'^(?P<event>[\w-]+)/create/$', RibbitCreateView, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', RibbitDetailSlugView.as_view(), name='read'),
    url(r'^$', RibbitListView.as_view(), name='list'),
]