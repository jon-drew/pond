from __future__ import unicode_literals

import random
import os

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from django.utils import timezone
from pond.utils import unique_slug_generator

from hoppers.models import Hopper

class Ribbit(models.Model):
    sent_by         = models.ForeignKey('hoppers.Hopper', on_delete=models.CASCADE, related_name='sender', null=True)
    event           = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    likes           = models.ManyToManyField('hoppers.Hopper', related_name='likes')
    spots           = models.ManyToManyField('hoppers.Hopper', related_name='spots')
    sent_to         = models.ManyToManyField('hoppers.Hopper', related_name='sent_to')
    slug            = models.SlugField(null=True, unique=True, editable=False)
    created_at      = models.DateTimeField(default=timezone.now)
    deleted_at      = models.DateTimeField(null=True)

    class Meta:
        unique_together = (('sent_by', 'event'),)
        ordering = ['-created_at']

    def __repr__(self):
        return str(self.sent_by) + '_' + str(self.event)

    def __str__(self):
        return str(self.sent_by) + '_' + str(self.event)

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Ribbit._meta.fields]

    def get_absolute_url(self):
        # Goes to self's details page
        return reverse('ribbits:read', kwargs={'slug': self.slug})

    def create_ribbit(self):
        # Creates a ribbit for the current user
        return reverse('ribbits:create_from_ribbit', kwargs={'ribbit': self.slug})

    def add_to_likes(self):
        # Adds the current user to the ribbit's likes field
        return reverse('ribbits:like', kwargs={'ribbit': self.slug})

    def add_to_spots(self):
        # Adds the current user to the ribbit's spots field
        return reverse('ribbits:spot', kwargs={'ribbit': self.slug})

    def get_likes_list(self):
        likes_list = self.likes.all()
        return Hopper.objects.filter(id__in=likes_list)

    def get_spots_list(self):
        spots_list = self.spots.all()
        return Hopper.objects.filter(id__in=spots_list)

def ribbit_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(ribbit_pre_save_receiver, sender=Ribbit)