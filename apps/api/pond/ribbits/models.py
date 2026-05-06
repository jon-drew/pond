from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from pond.utils import unique_slug_generator


class Ribbit(models.Model):
    sent_by = models.ForeignKey(
        'hoppers.Hopper',
        on_delete=models.CASCADE,
        related_name='sent_ribbits',
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='ribbits',
    )
    echo_of = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='echoes',
    )
    likes = models.ManyToManyField(
        'hoppers.Hopper',
        related_name='liked_ribbits',
        blank=True,
    )
    spots = models.ManyToManyField(
        'hoppers.Hopper',
        related_name='spotted_ribbits',
        blank=True,
    )
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('sent_by', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sent_by} @ {self.event}'

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    @property
    def score(self):
        return self.likes.count() + self.spots.count() * 3


def ribbit_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(ribbit_pre_save, sender=Ribbit)
