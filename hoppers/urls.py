from django.conf.urls import url

from .views import HopperUpdateView, PairCreateView, LoginRedirectView, HopperDetailSlugView, HopperListView

urlpatterns = [
    url(r'^update/$', HopperUpdateView, name='update'),
    url(r'^(?P<slug>[\w-]+)/listen/$', PairCreateView, name='create_pair'),
    url('login_redirect/$', LoginRedirectView, name='login_redirect'),
    url(r'^(?P<slug>[\w-]+)/$', HopperDetailSlugView.as_view(), name='read'),
    url(r'^$', HopperListView.as_view(), name='list'),
]