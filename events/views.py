from django.views.generic import UpdateView, ListView, DetailView
from django.http import Http404

from django.shortcuts import render, redirect

from .models import Event
from hoppers.models import Hopper
from pads.models import Pad

from .forms import EventCreateForm, EventUpdateForm

def EventCreateView(request):
    if request.method == "POST":
        form = EventCreateForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)

            # The event is always created by the current user, at their pad.
            created_by = Hopper.objects.get(user=request.user)
            event.created_by = created_by

            try:
                event.pad = Pad.objects.get(owner=created_by)
                event.save()
                if event.private == 1:
                    return redirect('ribbits:create_from_form', event=event.slug)
                return redirect('events:read', event.slug)
            except Pad.DoesNotExist:
                raise Http404('You must have a pad to create an event.')
    else:
        form = EventCreateForm()
        return render(request, 'events/create_event.html', {'form': form})

def EventUpdateView(request):
    if request.method == "POST":
        form = EventUpdateForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)

            # The event is always updated by the current user, at their pad.
            created_by = Hopper.objects.get(user=request.user)
            event.created_by = created_by

            try:
                event.pad = Pad.objects.get(owner=created_by)
                event.save()
                return redirect('events:read', event.slug)
            except Pad.DoesNotExist:
                raise Http404('You are not authorized to update this event.')
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
    template_name = 'events/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        hopper = Hopper.objects.get(user=request.user.id)
        return Event.objects.filter(attending=hopper).filter(created_by=hopper)
        #return Event.objects.exclude(created_by__id=request.user.id).filter(created_by__in=hopper.get_listens_to_list())