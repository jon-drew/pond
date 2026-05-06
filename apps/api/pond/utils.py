import random
import string
from django.utils.text import slugify


def random_string(size=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))


def unique_slug_generator(instance, new_slug=None):
    """Generate a unique slug for any model that has a `slug` and `name` (or `username`) field."""
    if new_slug is not None:
        slug = new_slug
    else:
        base = getattr(instance, 'name', None) or getattr(instance, 'username', None) or 'item'
        slug = slugify(base)

    ModelClass = instance.__class__
    qs = ModelClass.objects.filter(slug=slug).exclude(pk=instance.pk)
    if qs.exists():
        slug = f'{slug}-{random_string()}'
        return unique_slug_generator(instance, new_slug=slug)
    return slug
