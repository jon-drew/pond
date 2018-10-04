from django.views.generic import UpdateView, ListView, DetailView
from django.http import Http404

from django.shortcuts import render, redirect

from .models import Hopper, Listener
from .forms import HopperCreateForm, HopperUpdateForm, ListenerCreateForm

def HopperCreateView(request):
    if request.method == "POST":
        form = HopperCreateForm(request.POST)
        if form.is_valid():
            hopper = form.save(commit=False)
            hopper.save()
            return redirect('hoppers:read', hopper.slug)
    else:
        form = HopperCreateForm()
        return render(request, 'hoppers/create_hopper.html', {'form': form})

def HopperUpdateView(request):
    if request.method == "POST":
        form = HopperUpdateForm(request.POST)
        if form.is_valid():
            hopper = form.save(commit=False)
            hopper.save()
            return redirect('hoppers:read', hopper.slug)
    else:
        form = HopperUpdateForm()
        return render(request, 'hoppers/update_hopper.html', {'form': form})

class HopperDetailSlugView(DetailView):
    template_name = 'hoppers/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Hopper.objects.get(slug=slug, active=True)
        except Hopper.DoesNotExist:
            raise Http404('Hopper does not exist')
        except Hopper.MultipleObjectsReturned:
            qs = Hopper.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('Error in slug view')
        return instance

class HopperListView(ListView):
    queryset = Hopper.objects.all()
    template_name = 'hoppers/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Hopper.objects.all()

def ListenerCreateView(request):
    if request.method == "POST":
        form = ListenerCreateForm(request.POST)
        if form.is_valid():
            listener = form.save(commit=False)
            listener.save()
            return redirect('hoppers:list')
    else:
        form = ListenerCreateForm()
        return render(request, 'listeners/create_listener.html', {'form': form})

