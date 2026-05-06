from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from pond.utils import unique_slug_generator


class Pad(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    owner = models.ForeignKey(
        'hoppers.Hopper',
        null=True,
        on_delete=models.SET_NULL,
        related_name='pads',
    )
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.active = False
        self.save(update_fields=['deleted_at', 'active'])


def pad_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pad_pre_save, sender=Pad)
