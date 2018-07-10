from __future__ import unicode_literals

import random
import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator
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

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class EventQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()

    def get_absolute_url(self):
        return reverse('pads:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(event_pre_save_receiver, sender=Event)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

class EventQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()

class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)