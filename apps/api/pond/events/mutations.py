from datetime import datetime
from typing import Optional

import jwt
import strawberry
from strawberry.types import Info

from pond.events.models import Event
from pond.events.types import EventType
from pond.hoppers.tokens import decode_access_token
from pond.hoppers.models import Hopper
from pond.pads.models import Pad


def _require_auth(info: Info) -> Hopper:
    from django.conf import settings
    token = info.context.request.COOKIES.get(settings.ACCESS_TOKEN_COOKIE)
    if not token:
        raise PermissionError('Authentication required')
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise PermissionError('Token expired')
    except jwt.InvalidTokenError:
        raise PermissionError('Invalid token')
    return Hopper.objects.get(pk=payload['sub'])


@strawberry.type
class EventMutations:

    @strawberry.mutation
    def create_event(
        self,
        info: Info,
        title: str,
        text: str = '',
        start: Optional[str] = None,
        end: Optional[str] = None,
        pad_slug: Optional[str] = None,
        private: bool = True,
    ) -> EventType:
        me = _require_auth(info)
        pad = None
        if pad_slug:
            try:
                pad = Pad.objects.get(slug=pad_slug, deleted_at__isnull=True)
            except Pad.DoesNotExist:
                raise ValueError('Pad not found')
        kwargs = {'title': title, 'text': text, 'created_by': me, 'private': private}
        if pad:
            kwargs['pad'] = pad
        if start:
            kwargs['start'] = datetime.fromisoformat(start)
        if end:
            kwargs['end'] = datetime.fromisoformat(end)
        return Event.objects.create(**kwargs)

    @strawberry.mutation
    def update_event(
        self,
        info: Info,
        slug: str,
        title: Optional[str] = None,
        text: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        private: Optional[bool] = None,
    ) -> EventType:
        me = _require_auth(info)
        try:
            event = Event.objects.get(slug=slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValueError('Event not found')
        if event.created_by != me:
            raise PermissionError('Only the creator can update this event')
        if title is not None:
            event.title = title
        if text is not None:
            event.text = text
        if start is not None:
            event.start = datetime.fromisoformat(start)
        if end is not None:
            event.end = datetime.fromisoformat(end)
        if private is not None:
            event.private = private
        event.save()
        return event

    @strawberry.mutation
    def delete_event(self, info: Info, slug: str) -> bool:
        me = _require_auth(info)
        try:
            event = Event.objects.get(slug=slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValueError('Event not found')
        if event.created_by != me:
            raise PermissionError('Only the creator can delete this event')
        event.soft_delete()
        return True

    @strawberry.mutation
    def rsvp_event(self, info: Info, slug: str) -> EventType:
        me = _require_auth(info)
        try:
            event = Event.objects.get(slug=slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValueError('Event not found')
        if me in event.attending.all():
            event.attending.remove(me)
        else:
            event.attending.add(me)
        return event
