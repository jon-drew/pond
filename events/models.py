from django.db import models
from django.utils import timezone

from pads.models import Pad

def default_start():
  return timezone.now() + timezone.timedelta(days=1)

def default_end():
  return timezone.now() + timezone.timedelta(hours=1) + timezone.timedelta(days=1)

class Event(models.Model):
    start = models.DateTimeField(default=default_start)
    end = models.DateTimeField(default=default_end)
    pad = models.ForeignKey('pads.Pad', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title