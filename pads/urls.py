from django.conf.urls import url

from .views import PadCreateView, PadDetailSlugView, PadListView, PadUpdateView, PadDeleteView

urlpatterns = [
    url(r'^create/$', PadCreateView, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', PadDetailSlugView.as_view(), name='read'),
    url(r'^$', PadListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/update/$', PadUpdateView, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PadDeleteView, name='delete'),
]