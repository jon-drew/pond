from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from pond.utils import unique_slug_generator


def _default_start():
    return timezone.now() + timezone.timedelta(days=1)


def _default_end():
    return timezone.now() + timezone.timedelta(days=1, hours=1)


class Event(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    start = models.DateTimeField(default=_default_start)
    end = models.DateTimeField(default=_default_end)
    pad = models.ForeignKey(
        'pads.Pad',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='events',
    )
    created_by = models.ForeignKey(
        'hoppers.Hopper',
        null=True,
        on_delete=models.SET_NULL,
        related_name='created_events',
    )
    attending = models.ManyToManyField(
        'hoppers.Hopper',
        related_name='attending_events',
        blank=True,
    )
    private = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['start']

    def __str__(self):
        return self.title

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.active = False
        self.save(update_fields=['deleted_at', 'active'])

    def has_started(self):
        return self.start <= timezone.now()

    def has_ended(self):
        return self.end <= timezone.now()


def event_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(event_pre_save, sender=Event)
