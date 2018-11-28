from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import Http404
from django.shortcuts import render, redirect, render_to_response
from django.db import IntegrityError

from .models import Hopper, Pair
from .forms import HopperUpdateForm

def HopperUpdateView(request):
    # Inputs: an HTTP request
    # Function: processes a POST request to the hopper 'update' url
    # Returns: a redirect to the hopper 'read' url or HTTP404 error
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
        # Inputs: a GET request
        # Function: show the 'read' view for a hopper instance
        # Returns: a redirect to the hopper 'read' url or HTTP404 error
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            # Get the hopper instance from the url
            instance = Hopper.objects.get(slug=slug)
        except Hopper.DoesNotExist:
            raise Http404('Hopper does not exist')
        except Hopper.MultipleObjectsReturned:
            qs = Hopper.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404('Error in slug view')

        return instance

class HopperListView(ListView):
    template_name = 'hoppers/list.html'

    def get_queryset(self, *args, **kwargs):
        # Inputs: an GET request
        # Function: show a list of all the hoppers the current user doesn't already listen to
        # Returns: a redirect to the hopper 'list' url
        hopper = Hopper.objects.get(user=self.request.user.id)
        return Hopper.objects.exclude(id=hopper.id).exclude(id__in=self.request.user.hopper.listens_to.all())
        #return Hopper.objects.exclude(id=hopper.id).exclude(id__in=hopper.get_listens_to_list())

def PairCreateView(request, *args, **kwargs):
    # Inputs: an HTTP request
    # Function: processes a POST request to the hopper 'create_pair' url
    # Returns: a redirect to the pond 'login' url or HTTP404 error
    try:
        if request.user.is_authenticated:
            # Create new pairing
            first_hopper = Hopper.objects.get(user=request.user)
            second_hopper = Hopper.objects.get(slug=kwargs.get('slug'))
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
    # Inputs: an HTTP request
    # Function: processes a POST request to the pond 'login' url
    # Returns: a redirect to the hopper 'update' url if the user is anonymous or to the ribbit 'list' url if they are public
    is_anonymous = Hopper.objects.get(user=request.user).anonymous
    if is_anonymous == 1:
        return redirect('hoppers:update')
    else:
        return redirect('ribbits:list')
