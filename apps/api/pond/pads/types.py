import strawberry_django
from strawberry import auto

from pond.pads import models
from pond.hoppers.types import HopperType


@strawberry_django.type(models.Pad)
class PadType:
    id: auto
    name: auto
    address: auto
    description: auto
    owner: HopperType | None
    active: auto
    slug: auto
    created_at: auto
