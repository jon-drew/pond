from __future__ import unicode_literals

import random
import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from pond.utils import unique_slug_generator
from django.utils import timezone

from pads.models import Pad

def default_start():
  return timezone.now() + timezone.timedelta(days=1)

def default_end():
  return timezone.now() + timezone.timedelta(hours=1) + timezone.timedelta(days=1)

class Event(models.Model):
    start           = models.DateTimeField(default=default_start)
    end             = models.DateTimeField(default=default_end)
    pad             = models.ForeignKey('pads.Pad', on_delete=models.CASCADE)
    title           = models.CharField(max_length=200)
    text            = models.TextField()
    active          = models.BooleanField(default=True)
    slug            = models.SlugField(null=True, unique=True, editable=False)
    created_at      = models.DateTimeField(default=timezone.now)
    published_at    = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Event._meta.fields]

    def get_absolute_url(self):
        return reverse('events:read', kwargs={'slug': self.slug})

def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(event_pre_save_receiver, sender=Event)