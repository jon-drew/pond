from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.db.models import Q
from django.db.models.signals import pre_save, post_save

from django.urls import reverse

from django.dispatch import receiver

from pond.utils import unique_slug_generator
from django.utils import timezone

class Hopper(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    listener        = models.ManyToManyField('self', through='Listener', symmetrical=False)
    active          = models.BooleanField(default=True)
    slug            = models.SlugField(null=True, unique=True, editable=False)
    created_at      = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return self.slug

    def __str__(self):
        return str(self.user)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Hopper._meta.fields]

    def get_absolute_url(self):
        return reverse('hoppers:read', kwargs={'slug': self.slug})

def hopper_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(hopper_pre_save_receiver, sender=Hopper)

@receiver(post_save, sender=User)
def create_hopper(sender, instance, created, **kwargs):
    if created:
        Hopper.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_Hopper(sender, instance, **kwargs):
    instance.hopper.save()


class Listener(models.Model):
    first_hopper = models.ForeignKey(Hopper, null=True, on_delete=models.SET_NULL, related_name='first_hopper')
    second_hopper = models.ForeignKey(Hopper, null=True, on_delete=models.SET_NULL, related_name='second_hopper')
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return u'%s, %s' % (self.first_hopper, self.second_hopper)