from django.views.generic import UpdateView, ListView, DetailView
from django.http import Http404

from django.shortcuts import render, redirect

from .models import Pad
from .forms import PadCreateForm, PadUpdateForm

# Create your views here.

def PadCreateView(request):
    if request.method == "POST":
        form = PadCreateForm(request.POST)
        if form.is_valid():
            pad = form.save(commit=False)
            pad.save()
            return redirect('pads:read', pad.slug)
    else:
        form = PadCreateForm()
        return render(request, 'pads/create_pad.html', {'form': form})

def PadUpdateView(request):
    if request.method == "POST":
        form = PadUpdateForm(request.POST)
        if form.is_valid():
            pad = form.save(commit=False)
            pad.save()
            return redirect('pads:read', pad.slug)
    else:
        form = PadUpdateForm()
        return render(request, 'pads/update_pad.html', {'form': form})

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
        return Pad.objects.all()