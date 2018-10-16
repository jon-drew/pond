from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import Http404
from django.shortcuts import render, redirect, render_to_response
from django.db import IntegrityError

from .models import Hopper, Pair
from .forms import HopperUpdateForm

def HopperUpdateView(request):
    try:
        hopper = request.user.hopper
    except UserProfile.DoesNotExist:
        hopper = Hopper(user=request.user)

    try:
        if request.method == "POST":
            form = HopperUpdateForm(request.POST, instance=hopper)
            if form.is_valid():
                hopper = form.save(commit=False)
                hopper.save()
                return redirect('hoppers:read', hopper.slug)
        else:
            form = HopperUpdateForm()
            return render(request, 'hoppers/update_hopper.html', {'form': form})
    except:
        raise Http404('Error in slug view.')

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
    template_name = 'hoppers/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request.user.id
        hopper = Hopper.objects.get(user=request)
        #return Hopper.objects.all()
        return Hopper.objects.exclude(id=hopper.id).exclude(id__in=hopper.get_listens_to_list())

def PairCreateView(request, *args, **kwargs):
    try:
        if request.user.is_authenticated:
            # Create new pairing
            first_hopper = Hopper.objects.get(slug=kwargs.get('slug'))
            second_hopper = Hopper.objects.get(user=request.user)
            new_pair = Pair(first_hopper=first_hopper, second_hopper=second_hopper)
            new_pair.save()

            return redirect('hoppers:list')
        else:
            return redirect('login')
    except IntegrityError:
        return redirect('hoppers:list')
    except:
        raise Http404('Error adding pairing.')

def LoginRedirectView(request):
    """Redirector to figure out where the user goes next."""
    is_anonymous = Hopper.objects.get(user=request.user).anonymous
    if is_anonymous == 1:
        return redirect('hoppers:update')
    else:
        return redirect('ribbits:list')
