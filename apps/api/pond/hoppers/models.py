import secrets
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify


class Hopper(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    anonymous = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    listens_to = models.ManyToManyField(
        'self',
        through='Pair',
        symmetrical=False,
        related_name='listened_by',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    @property
    def is_public(self):
        return not self.anonymous


class Pair(models.Model):
    first_hopper = models.ForeignKey(Hopper, on_delete=models.CASCADE, related_name='following_set')
    second_hopper = models.ForeignKey(Hopper, on_delete=models.CASCADE, related_name='follower_set')

    class Meta:
        unique_together = ('first_hopper', 'second_hopper')

    def __str__(self):
        return f'{self.first_hopper} -> {self.second_hopper}'


class RefreshToken(models.Model):
    hopper = models.ForeignKey(Hopper, on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.CharField(max_length=128, unique=True, db_index=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def issue(cls, hopper: 'Hopper') -> 'RefreshToken':
        from django.conf import settings
        token_str = secrets.token_urlsafe(64)
        expires_at = timezone.now() + timedelta(seconds=settings.REFRESH_TOKEN_LIFETIME_SECONDS)
        return cls.objects.create(hopper=hopper, token=token_str, expires_at=expires_at)

    def is_valid(self) -> bool:
        return self.expires_at > timezone.now()

    def __str__(self):
        return f'{self.hopper.username} token'


def hopper_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        base = slugify(instance.username)
        slug = base
        n = 1
        while Hopper.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f'{base}-{n}'
            n += 1
        instance.slug = slug
    if instance.email and instance.name and instance.birth_date:
        instance.anonymous = False


pre_save.connect(hopper_pre_save, sender=Hopper)
