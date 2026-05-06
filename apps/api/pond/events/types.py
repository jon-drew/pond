import strawberry_django
from strawberry import auto

from pond.events import models
from pond.hoppers.types import HopperType
from pond.pads.types import PadType


@strawberry_django.type(models.Event)
class EventType:
    id: auto
    title: auto
    text: auto
    start: auto
    end: auto
    pad: PadType | None
    created_by: HopperType | None
    attending: list[HopperType]
    private: auto
    active: auto
    slug: auto
    created_at: auto
