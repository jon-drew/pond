from __future__ import unicode_literals

import random
import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from pond.utils import unique_slug_generator
from django.utils import timezone

class Pad(models.Model):
    name            = models.CharField(default="My Pad", max_length=50)
    address         = models.CharField(max_length=200)
    description     = models.TextField(max_length=200)
    active          = models.BooleanField(default=True)
    slug            = models.SlugField(null=True, unique=True)
    created_at      = models.DateTimeField(default=timezone.now)
    published_at    = models.DateTimeField(blank=True, null=True)

    def __repr__(self):
        return self.slug

    def __str__(self):
        return self.name

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Pad._meta.fields]

    def get_absolute_url(self):
        return reverse('pads:read', kwargs={'slug': self.slug})

def pad_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pad_pre_save_receiver, sender=Pad)
