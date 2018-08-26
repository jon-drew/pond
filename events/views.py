from django.views.generic import UpdateView, ListView, DetailView
from django.http import Http404

from django.shortcuts import render, redirect

from .models import Event
from .forms import EventCreateForm, EventUpdateForm

# Create your views here.

def EventCreateView(request):
    if request.method == "POST":
        form = EventCreateForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('events:read', event.slug)
    else:
        form = EventCreateForm()
        return render(request, 'events/create_event.html', {'form': form})

def EventUpdateView(request):
    if request.method == "POST":
        form = EventUpdateForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('events:read', event.slug)
    else:
        form = EventUpdateForm()
        return render(request, 'events/update_event.html', {'form': form})

class EventDetailSlugView(DetailView):
    template_name = 'events/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Event.objects.get(slug=slug, active=True)
        except Event.DoesNotExist:
            raise Http404('Event does not exist')
        except Event.MultipleObjectsReturned:
            qs = Event.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('Error in slug view')
        return instance

class EventListView(ListView):
    queryset = Event.objects.all()
    template_name = 'events/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Event.objects.all()