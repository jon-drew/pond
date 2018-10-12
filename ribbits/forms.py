from .models import Ribbit
from django.forms import ModelForm

class RibbitCreateForm(ModelForm):
    class Meta:
        model = Ribbit
        fields = ['event']