from typing import Optional

import strawberry
from strawberry.types import Info

from pond.events.models import Event
from pond.events.types import EventType
from pond.hoppers.tokens import decode_access_token
from pond.hoppers.models import Hopper


def _get_current_hopper(info: Info) -> Optional[Hopper]:
    from django.conf import settings
    import jwt
    token = info.context.request.COOKIES.get(settings.ACCESS_TOKEN_COOKIE)
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        return Hopper.objects.get(pk=payload['sub'])
    except Exception:
        return None


@strawberry.type
class EventQueries:

    @strawberry.field
    def events(self, info: Info) -> list[EventType]:
        me = _get_current_hopper(info)
        qs = Event.objects.filter(deleted_at__isnull=True, active=True)
        if me:
            from django.db.models import Q
            return qs.filter(Q(private=False) | Q(created_by=me) | Q(attending=me)).distinct()
        return qs.filter(private=False)

    @strawberry.field
    def event(self, slug: str) -> Optional[EventType]:
        try:
            return Event.objects.get(slug=slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            return None
