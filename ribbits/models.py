from __future__ import unicode_literals

import random
import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from django.utils import timezone
from pond.utils import unique_slug_generator

from events.models import Event

class Ribbit(models.Model):
    sent_by         = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sender')
    got_by          = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='receiver')
    event           = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    response        = models.BooleanField(default=0)
    title           = models.CharField(default='_', max_length=200)
    active          = models.BooleanField(default=True)
    slug            = models.SlugField(null=True, unique=True, editable=False)
    created_at      = models.DateTimeField(default=timezone.now)
    published_at    = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.slug

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def responded(self):
        return bool(self.response)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Ribbit._meta.fields]

    def get_absolute_url(self):
        return reverse('ribbits:read', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

def ribbit_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.title:
        instance.title = '_'.join([str(instance.sent_by), str(instance.got_by), str(instance.title)])
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(ribbit_pre_save_receiver, sender=Ribbit)