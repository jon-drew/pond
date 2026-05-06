import jwt
import strawberry
from strawberry.types import Info

from pond.ribbits.models import Ribbit
from pond.ribbits.types import RibbitType
from pond.events.models import Event
from pond.hoppers.tokens import decode_access_token
from pond.hoppers.models import Hopper


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
class RibbitMutations:

    @strawberry.mutation
    def create_ribbit(self, info: Info, event_slug: str) -> RibbitType:
        me = _require_auth(info)
        try:
            event = Event.objects.get(slug=event_slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValueError('Event not found')
        ribbit, _ = Ribbit.objects.get_or_create(sent_by=me, event=event)
        return ribbit

    @strawberry.mutation
    def like_ribbit(self, info: Info, slug: str) -> RibbitType:
        me = _require_auth(info)
        try:
            ribbit = Ribbit.objects.get(slug=slug, deleted_at__isnull=True)
        except Ribbit.DoesNotExist:
            raise ValueError('Ribbit not found')
        if me in ribbit.likes.all():
            ribbit.likes.remove(me)
        else:
            ribbit.likes.add(me)
        return ribbit

    @strawberry.mutation
    def spot_ribbit(self, info: Info, slug: str) -> RibbitType:
        me = _require_auth(info)
        try:
            ribbit = Ribbit.objects.get(slug=slug, deleted_at__isnull=True)
        except Ribbit.DoesNotExist:
            raise ValueError('Ribbit not found')
        if me in ribbit.spots.all():
            ribbit.spots.remove(me)
        else:
            ribbit.spots.add(me)
        return ribbit

    @strawberry.mutation
    def echo_ribbit(self, info: Info, slug: str) -> RibbitType:
        me = _require_auth(info)
        try:
            source = Ribbit.objects.select_related('sent_by', 'event').get(
                slug=slug, deleted_at__isnull=True
            )
        except Ribbit.DoesNotExist:
            raise ValueError('Ribbit not found')
        if source.sent_by == me:
            raise ValueError('Cannot echo your own Ribbit')
        ribbit, created = Ribbit.objects.get_or_create(
            sent_by=me,
            event=source.event,
            defaults={'echo_of': source},
        )
        if not created:
            ribbit.echo_of = source
            ribbit.save(update_fields=['echo_of'])
        return ribbit
