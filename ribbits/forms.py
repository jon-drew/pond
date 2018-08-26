from .models import Ribbit
from django.forms import ModelForm

class RibbitCreateForm(ModelForm):
    class Meta:
        model = Ribbit
        fields = ['sent_by', 'got_by', 'event', 'response']

class RibbitUpdateForm(ModelForm):
    class Meta:
        model = Ribbit
        fields = ['sent_by', 'got_by', 'event', 'response']