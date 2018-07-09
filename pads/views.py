from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import render

from .models import Pad
# Create your views here.

class PadListView(ListView):
    queryset = Pad.objects.all()
    template_name = 'pads/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Pad.objects.all()


class PadDetailView(DetailView):
    template_name = "pads/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(padDetailView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Pad.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Pad doesn't exist")
        return instance

class PadDetailSlugView(DetailView):
    template_name = 'pads/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Pad.objects.get(slug=slug, active=True)
        except pad.DoesNotExist:
            raise Http404('Pad does not exist')
        except Pad.MultipleObjectsReturned:
            qs = Pad.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('Error in slug view')
        return instance
