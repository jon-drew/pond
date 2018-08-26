from .models import Event
from django.forms import ModelForm

class EventCreateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['start', 'end', 'pad', 'title', 'text']

class EventUpdateForm(ModelForm):
    class Meta:
        model = Event
        fields = ['start', 'end', 'pad', 'title', 'text']