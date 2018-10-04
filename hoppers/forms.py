from .models import Hopper, Listener
from django.contrib.auth.models import User

from django.forms import ModelForm

class HopperCreateForm(ModelForm):
    class Meta:
        model = User
        fields = ()

class HopperUpdateForm(ModelForm):
    class Meta:
        model = Hopper
        fields = ()

class ListenerCreateForm(ModelForm):
    class Meta:
        model = Listener
        fields = ()