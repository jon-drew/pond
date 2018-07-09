from __future__ import unicode_literals

import random
import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator
from django.utils import timezone

class Pad(models.Model):
    address         = models.TextField()
    owner           = models.CharField(max_length=200)
    description     = models.TextField()
    active          = models.BooleanField(default=True)
    created_at      = models.DateTimeField(default=timezone.now)
    published_at    = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class PadQuerySet(models.query.QuerySet):
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


def pad_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pad_pre_save_receiver, sender=Pad)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 999999)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'pads/{new_filename}/{final_filename}'.format(
            new_filename=new_filename,
            final_filename=final_filename
            )

class PadQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()

class PadManager(models.Manager):
    def get_queryset(self):
        return PadQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)