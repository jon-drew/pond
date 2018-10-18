from django.conf.urls import url

from .views import RibbitCreateView, RibbitCreateFromFormView, RibbitListView, RibbitDetailSlugView, LikeCreateView, SpotCreateView

urlpatterns = [
    url(r'^(?P<event>[\w-]+)/create/$', RibbitCreateView, name='create'),
    url(r'^(?P<event>[\w-]+)/create_from_form/$', RibbitCreateFromFormView, name='create_from_form'),
    url(r'^(?P<slug>[\w-]+)/$', RibbitDetailSlugView.as_view(), name='read'),
    url(r'^$', RibbitListView.as_view(), name='list'),
    url(r'^(?P<ribbit>[\w-]+)/like/$', LikeCreateView, name='like'),
    url(r'^(?P<ribbit>[\w-]+)/spot/$', SpotCreateView, name='spot'),
]