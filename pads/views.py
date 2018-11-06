from django.views.generic import UpdateView, ListView, DetailView
from django.http import Http404
from django.db import IntegrityError

from django.shortcuts import render, redirect

from .models import Pad
from hoppers.models import Hopper

from .forms import PadCreateForm, PadUpdateForm

def PadCreateView(request):
    if request.method == "POST":
        try:
            form = PadCreateForm(request.POST)
            if form.is_valid():
                pad = form.save(commit=False)
                # The pad is always created by the current user.
                pad.owner = Hopper.objects.get(user=request.user)
                pad.save()
                return redirect('pads:read', pad.slug)
        except IntegrityError:
            return Http404('One pad per user.')

    else:
        form = PadCreateForm()
        return render(request, 'pads/create_pad.html', {'form': form})

class PadDetailSlugView(DetailView):
    template_name = 'pads/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Pad.objects.get(slug=slug, active=True)
        except Pad.DoesNotExist:
            raise Http404('Pad does not exist')
        except Pad.MultipleObjectsReturned:
            qs = Pad.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('Error in slug view')
        return instance

class PadListView(ListView):
    queryset = Pad.objects.all()
    template_name = 'pads/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Pad.objects.exclude(active=False)

def PadUpdateView(request, slug):
    try:
        pad = request.user.hopper.pad
    except:
        return Http404('You do not have a pad to update.')

    try:
        if request.method == "POST":
            form = PadUpdateForm(request.POST, instance=pad)
            if form.is_valid():
                pad = form.save(commit=False)
                pad.save()
                return redirect('pads:read', pad.slug)
        else:
            form = PadUpdateForm()
            return render(request, 'pads/update_pad.html', {'form': form})
    except:
        raise Http404('Error in update view.')

def PadDeleteView(request, slug):
    try:
        pad = request.user.hopper.pad
    except:
        return Http404('You do not have a pad to delete.')

    try:
        pad.active = False
        pad.save()
        return redirect('pads:list')
    except:
        raise Http404('Error in delete view.')