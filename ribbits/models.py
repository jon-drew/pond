from __future__ import unicode_literals

import random
import os

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from django.utils import timezone
from pond.utils import unique_slug_generator

class Ribbit(models.Model):
    sent_by         = models.ForeignKey('hoppers.Hopper', on_delete=models.CASCADE, related_name='sender', null=True)
    event           = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    slug            = models.SlugField(null=True, unique=True, editable=False)
    created_at      = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('sent_by', 'event'),)
        ordering = ['-created_at']

    def __repr__(self):
        return self.slug

    def __str__(self):
        return str(self.slug)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Ribbit._meta.fields]

    def get_absolute_url(self):
        return reverse('ribbits:read', kwargs={'slug': self.slug})

    def respond(self):
        # Creates a ribbit for the current user
        return reverse('ribbits:create', kwargs={'event': self.event.slug})

def ribbit_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(ribbit_pre_save_receiver, sender=Ribbit)