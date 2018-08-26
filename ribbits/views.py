from django.views.generic import UpdateView, ListView, DetailView
from django.http import Http404

from django.shortcuts import render, redirect

from .models import Ribbit
from .forms import RibbitCreateForm, RibbitUpdateForm

# Create your views here.

def RibbitCreateView(request):
    if request.method == "POST":
        form = RibbitCreateForm(request.POST)
        if form.is_valid():
            ribbit = form.save(commit=False)
            ribbit.save()
            return redirect('ribbits:read', ribbit.slug)
    else:
        form = RibbitCreateForm()
        return render(request, 'ribbits/create_Ribbit.html', {'form': form})

def RibbitUpdateView(request):
    if request.method == "POST":
        form = RibbitUpdateForm(request.POST)
        if form.is_valid():
            ribbit = form.save(commit=False)
            ribbit.save()
            return redirect('ribbits:read', ribbit.slug)
    else:
        form = RibbitUpdateForm()
        return render(request, 'ribbits/update_Ribbit.html', {'form': form})

class RibbitDetailSlugView(DetailView):
    template_name = 'Ribbits/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Ribbit.objects.get(slug=slug, active=True)
        except Ribbit.DoesNotExist:
            raise Http404('Ribbit does not exist')
        except Ribbit.MultipleObjectsReturned:
            qs = Ribbit.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('Error in slug view')
        return instance

class RibbitListView(ListView):
    queryset = Ribbit.objects.all()
    template_name = 'Ribbits/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Ribbit.objects.all()