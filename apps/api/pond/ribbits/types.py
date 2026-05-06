from __future__ import annotations
from typing import Optional

import strawberry
import strawberry_django
from strawberry import auto

from pond.ribbits import models
from pond.hoppers.types import HopperType
from pond.events.types import EventType


@strawberry_django.type(models.Ribbit)
class RibbitType:
    id: auto
    sent_by: HopperType
    event: EventType
    echo_of: Optional['RibbitType']
    likes: list[HopperType]
    spots: list[HopperType]
    slug: auto
    created_at: auto

    @strawberry_django.field
    def score(self) -> int:
        return self.likes.count() + self.spots.count() * 3

    @strawberry_django.field
    def echo_count(self) -> int:
        return self.echoes.filter(deleted_at__isnull=True).count()


@strawberry.type
class RibbitPatternNodeType:
    ribbit: RibbitType
    parent_slug: Optional[str]
    depth: int
    direct_echo_count: int
    total_echo_count: int
    score: int
