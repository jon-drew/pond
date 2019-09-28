from .models import Hopper

from django import forms
from django.forms import ModelForm

class HopperUpdateForm(ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Hopper
        fields = ['name', 'email', 'birth_date', 'includes', 'excludes', 'image']