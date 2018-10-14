from django.conf.urls import url

from .views import PadCreateView, PadUpdateView, PadListView, PadDetailSlugView

urlpatterns = [
    url(r'^create/$', PadCreateView, name='create'),
    url(r'^update/$', PadUpdateView, name='update'),
    url(r'^(?P<slug>[\w-]+)/$', PadDetailSlugView.as_view(), name='read'),
    url(r'^$', PadListView.as_view(), name='list'),
]