from .models import Pad
from django.forms import ModelForm

class PadCreateForm(ModelForm):
    class Meta:
        model = Pad
        fields = ['name', 'address', 'description']

class PadUpdateForm(ModelForm):
    class Meta:
        model = Pad
        fields = ['name', 'address', 'description']