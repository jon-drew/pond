from typing import Optional

import strawberry

from pond.pads.models import Pad
from pond.pads.types import PadType


@strawberry.type
class PadQueries:

    @strawberry.field
    def pads(self) -> list[PadType]:
        return Pad.objects.filter(active=True, deleted_at__isnull=True)

    @strawberry.field
    def pad(self, slug: str) -> Optional[PadType]:
        try:
            return Pad.objects.get(slug=slug, deleted_at__isnull=True)
        except Pad.DoesNotExist:
            return None
