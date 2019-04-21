import datetime

from django.views.generic import UpdateView, ListView, DetailView
from django.http import Http404

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from .models import Event
from hoppers.models import Hopper
from pads.models import Pad

from .forms import EventCreateForm, EventUpdateForm

from pond.utils import random_string_generator

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

class EventDetailSlugView(DetailView):
    template_name = 'events/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # get_object_or_404(Event, slug=slug)
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
        hopper = Hopper.objects.get(user=request.user)
        # Returns list of ribbit objects from hoppers the current user listens to
        attending = Event.objects.filter(attending=hopper).filter(end__gte=datetime.datetime.now()).filter(active=True)
        created = Event.objects.filter(created_by=hopper).filter(end__gte=datetime.datetime.now()).filter(active=True)
        return attending | created

def EventUpdateView(request, slug):
    try:
        event = Event.objects.get(slug=slug)
        if request.user.hopper != event.created_by:
            raise Http404('You are not authorized to delete this event.')

        elif request.method == "POST":
            form = EventUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)

                # Assigning form values to event
                event.start = form.start
                event.end = form.end
                event.title = form.title
                event.text = form.text
                event.private = form.private
                event.image = form.image
                event.caption = form.caption
                event.slug = slugify(form.title + '_' + random_string_generator())

                # The pad is always updated by the current user, at their pad.
                event.created_by = Hopper.objects.get(user=request.user)
                event.pad = Pad.objects.get(owner=request.user.hopper)
                event.save()
                if event.private == 1:
                    return redirect('ribbits:create_from_form', event=event.slug)
                return redirect('events:read', event.slug)
        else:
            form = EventUpdateForm()
            return render(request, 'events/update_event.html', {'form': form})
    except Event.DoesNotExist:
        raise Http404('That event does not exist.')

def EventDeleteView(request, slug):
    try:
        event = Event.objects.get(slug=slug)
        if request.user.hopper != event.created_by:
            raise Http404('You are not authorized to delete this event.')
        else:
            event.active = False
            event.save()
            return redirect('events:list')
    except Event.DoesNotExist:
        raise Http404('That event does not exist.')