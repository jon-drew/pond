from django.conf.urls import url

from .views import RibbitRibbitCreateView, RibbitFormCreateView, RibbitListView, RibbitDetailSlugView, LikeCreateView, SpotCreateView

urlpatterns = [
    url(r'^(?P<ribbit>[\w-]+)/create/$', RibbitRibbitCreateView, name='create_from_ribbit'),
    url(r'^(?P<event>[\w-]+)/create_from_form/$', RibbitFormCreateView, name='create_from_form'),
    url(r'^$', RibbitListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', RibbitDetailSlugView.as_view(), name='read'),
    url(r'^(?P<ribbit>[\w-]+)/like/$', LikeCreateView, name='like'),
    url(r'^(?P<ribbit>[\w-]+)/spot/$', SpotCreateView, name='spot'),
]