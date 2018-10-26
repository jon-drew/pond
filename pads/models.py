from __future__ import unicode_literals

import random
import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from pond.utils import unique_slug_generator
from django.utils import timezone

from events.models import Event
from hoppers.models import Hopper

class Pad(models.Model):
    name            = models.CharField(max_length=20)
    address         = models.CharField(max_length=100)
    description     = models.TextField(max_length=200)
    owner           = models.OneToOneField(Hopper, null=True, on_delete=models.SET_NULL)
    active          = models.BooleanField(default=True)
    slug            = models.SlugField(null=True, unique=True, editable=False)
    created_at      = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Pad._meta.fields]

    def get_absolute_url(self):
        return reverse('pads:read', kwargs={'slug': self.slug})

    def get_events_list(self):
        return Event.objects.filter(pad=self).exclude(private=1)

def pad_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pad_pre_save_receiver, sender=Pad)
