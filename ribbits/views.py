from django.views.generic import UpdateView, ListView, DetailView
from django.http import Http404
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages

from .models import Ribbit
from hoppers.models import Hopper
from events.models import Event

from .forms import RibbitCreateForm

def RibbitCreateView(request, *args, **kwargs):
    try:
        if request.user.is_authenticated:

            # Create new ribbit
            sent_by = Hopper.objects.get(user=request.user)
            event = Event.objects.get(slug=kwargs.get('event'))
            new_ribbit = Ribbit(sent_by=sent_by, event=event)
            new_ribbit.save()

            # Add user to event
            event.attending.add(sent_by)

            return redirect('ribbits:list')
        else:
            return redirect('login')
    except IntegrityError:
        return redirect('ribbits:list')
    except:
        raise Http404('Error creating ribbit.')

class RibbitDetailSlugView(DetailView):
    template_name = 'Ribbits/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            if request.user.is_authenticated:
                instance = Ribbit.objects.get(slug=slug)
            else:
                return redirect('login')
        except Ribbit.DoesNotExist:
            raise Http404('Ribbit does not exist')
        except Ribbit.MultipleObjectsReturned:
            qs = Ribbit.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404('Error in slug view')
        return instance

class RibbitListView(ListView):
    template_name = 'ribbits/list.html'

    def get_queryset(self, *args, **kwargs):
        hopper = Hopper.objects.get(user=self.request.user.id)
        # Returns list of ribbit objects from hoppers the current user listens to
        return Ribbit.objects.exclude(event__private=1).exclude(sent_by=hopper).filter(sent_by__in=hopper.get_listens_to_list())

def LikeCreateView(request, *args, **kwargs):
    try:
        if request.user.is_authenticated:

            # Add user to likes
            sent_by = Hopper.objects.get(user=request.user)
            ribbit = Ribbit.objects.get(slug=kwargs.get('ribbit'))
            ribbit.likes.add(sent_by)
            return redirect('ribbits:list')
        else:
            return redirect('login')
    except IntegrityError:
        return redirect('ribbits:list')
    except:
        raise Http404('Error liking that ribbit.')

def SpotCreateView(request, *args, **kwargs):
    try:
        if request.user.is_authenticated:

            # Add user to spots
            sent_by = Hopper.objects.get(user=request.user)
            ribbit = Ribbit.objects.get(slug=kwargs.get('ribbit'))
            ribbit.spots.add(sent_by)
            return redirect('ribbits:list')
        else:
            return redirect('login')
    except IntegrityError:
        return redirect('ribbits:list')
    except:
        raise Http404('Error spotting that ribbit.')