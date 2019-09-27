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
    user            = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    listens_to      = models.ManyToManyField('self', through='Pair', symmetrical=False)
    anonymous       = models.BooleanField(default=True)
    email           = models.EmailField(null=True, max_length=100)
    name            = models.CharField(null=True, max_length=100)
    birth_date      = models.DateField(null=True, blank=True)
    includes        = models.TextField(null=True, blank=True)
    excludes        = models.TextField(null=True, blank=True)
    slug            = models.SlugField(null=True, blank=True, unique=True, editable=False)
    created_at      = models.DateTimeField(default=timezone.now)
    image           = models.ImageField(null=True, blank=True)

    def __repr__(self):
        return str(self.user.username)

    def __str__(self):
        if self.anonymous:
            return str(self.user.username)
        else:
            return str(self.name)

    def get_fields(self):
        # Inputs: self
        # Function: shows field-value pairings for hopper object
        # Returns: a list of of lists, each containing two strings ['field.name', 'field.value_to_string']
        return [(field.name, field.value_to_string(self)) for field in Hopper._meta.fields]

    def get_absolute_url(self):
        # Inputs: self
        # Function: provides the read url for the hopper object
        # Returns: a url associated with the hopper object
        return reverse('hoppers:read', kwargs={'slug': self.slug})

    def get_listens_to_list(self):
        # Inputs: self
        # Function: find all the other hoppers self is listening to
        # Returns: a list of hopper objects
        return Hopper.objects.filter(id__in=self.listens_to.all())

    def get_count_of_listens_to_list(self):
        # Inputs: self
        # Function: counts how many other hoppers self is listening to
        # Returns: an integer
        return Hopper.objects.filter(id__in=self.listens_to.all()).count()

    def add_pair(self):
        # Inputs: self
        # Function: creates a new object in the Pairs table
        # Returns: none
        return reverse('hoppers:create_pair', kwargs={'slug': self.slug})

    def is_past_delete_date(self):
        # TODO: Implement deletion of old accounts.
        pass

def hopper_pre_save_receiver(sender, instance, *args, **kwargs):
    # Inputs: a hopper object as sender and instance
    # Function: creates a slug if none exists and sets the accounts anonymous field
    # Returns: none
    if not instance.slug:
        # Uses the unique slug generator from pond/utils to create a slug if one does not already exist.
        instance.slug = unique_slug_generator(instance)
    if instance.email and instance.name and instance.birth_date:
        # A hopper must provide all 3 pieces of information to go from anonymous to public.
        instance.anonymous = False

pre_save.connect(hopper_pre_save_receiver, sender=Hopper)

@receiver(post_save, sender=User)
def create_hopper(sender, instance, created, **kwargs):
    if created:
        Hopper.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_Hopper(sender, instance, **kwargs):
    instance.hopper.save()

class Pair(models.Model):
    first_hopper = models.ForeignKey(Hopper, on_delete=models.CASCADE, related_name='first_hopper')
    second_hopper = models.ForeignKey(Hopper, on_delete=models.CASCADE, related_name='second_hopper')

    class Meta:
        unique_together = (('first_hopper', 'second_hopper'),)

    def __repr__(self):
        return  '_'.join([str(self.first_hopper), str(self.second_hopper)])

    def __str__(self):
        return  '_'.join([str(self.first_hopper), str(self.second_hopper)])