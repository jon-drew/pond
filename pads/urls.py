from django.conf.urls import url

from .views import PadListView, PadDetailSlugView

urlpatterns = [
    url(r'^$', PadListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', PadDetailSlugView.as_view(), name='detail'),
]