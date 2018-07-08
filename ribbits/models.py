from django.db import models
from django.utils import timezone

from events.models import Event

class Ribbit(models.Model):
    sent_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='sender')
    got_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='receiver')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    response = models.BooleanField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

    def responded(self):
        return bool(self.response)