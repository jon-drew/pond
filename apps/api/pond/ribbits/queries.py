from typing import Optional

import strawberry
from strawberry.types import Info

from pond.ribbits.models import Ribbit
from pond.ribbits.types import RibbitType, RibbitPatternNodeType
from pond.events.models import Event
from pond.hoppers.models import Hopper


def _require_auth(info: Info) -> Hopper:
    from django.conf import settings
    import jwt
    from pond.hoppers.tokens import decode_access_token
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
class RibbitQueries:

    @strawberry.field
    def ribbits(self, info: Info) -> list[RibbitType]:
        me = _require_auth(info)
        following_ids = me.listens_to.values_list('id', flat=True)
        from django.db.models import Q
        return Ribbit.objects.filter(
            deleted_at__isnull=True
        ).filter(
            Q(sent_by__in=following_ids) | Q(sent_by=me)
        ).select_related('sent_by', 'event', 'echo_of').prefetch_related('likes', 'spots')

    @strawberry.field
    def ribbit(self, slug: str) -> Optional[RibbitType]:
        try:
            return Ribbit.objects.get(slug=slug, deleted_at__isnull=True)
        except Ribbit.DoesNotExist:
            return None

    @strawberry.field
    def event_ribbit_pattern(self, info: Info, event_slug: str) -> list[RibbitPatternNodeType]:
        me = _require_auth(info)
        try:
            event = Event.objects.get(slug=event_slug, deleted_at__isnull=True)
        except Event.DoesNotExist:
            raise ValueError('Event not found')
        if event.created_by_id != me.pk:
            raise PermissionError('Only the event owner can view patterns')

        ribbits = list(
            Ribbit.objects.filter(event=event, deleted_at__isnull=True)
            .select_related('sent_by', 'echo_of')
            .prefetch_related('likes', 'spots')
        )

        slug_to_ribbit = {r.slug: r for r in ribbits}
        slug_to_children: dict[str, list[str]] = {r.slug: [] for r in ribbits}
        for r in ribbits:
            if r.echo_of_id:
                parent = r.echo_of
                if parent and parent.slug in slug_to_children:
                    slug_to_children[parent.slug].append(r.slug)

        def total_count(slug: str) -> int:
            children = slug_to_children.get(slug, [])
            return len(children) + sum(total_count(c) for c in children)

        def get_depth(ribbit: Ribbit) -> int:
            d = 0
            cur = ribbit
            visited = set()
            while cur.echo_of_id:
                if cur.slug in visited:
                    break
                visited.add(cur.slug)
                d += 1
                cur = slug_to_ribbit.get(cur.echo_of.slug if cur.echo_of else '', cur)
                if d > 50:
                    break
            return d

        return [
            RibbitPatternNodeType(
                ribbit=r,
                parent_slug=r.echo_of.slug if r.echo_of_id and r.echo_of else None,
                depth=get_depth(r),
                direct_echo_count=len(slug_to_children[r.slug]),
                total_echo_count=total_count(r.slug),
                score=r.likes.count() + r.spots.count() * 3,
            )
            for r in ribbits
        ]
