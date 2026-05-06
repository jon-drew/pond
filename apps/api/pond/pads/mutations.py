from typing import Optional

import jwt
import strawberry
from strawberry.types import Info

from pond.pads.models import Pad
from pond.pads.types import PadType
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
class PadMutations:

    @strawberry.mutation
    def create_pad(self, info: Info, name: str, address: str, description: str = '') -> PadType:
        me = _require_auth(info)
        return Pad.objects.create(name=name, address=address, description=description, owner=me)

    @strawberry.mutation
    def update_pad(
        self,
        info: Info,
        slug: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
    ) -> PadType:
        me = _require_auth(info)
        try:
            pad = Pad.objects.get(slug=slug, deleted_at__isnull=True)
        except Pad.DoesNotExist:
            raise ValueError('Pad not found')
        if pad.owner != me:
            raise PermissionError('Only the owner can update this pad')
        if name is not None:
            pad.name = name
        if address is not None:
            pad.address = address
        if description is not None:
            pad.description = description
        pad.save()
        return pad

    @strawberry.mutation
    def delete_pad(self, info: Info, slug: str) -> bool:
        me = _require_auth(info)
        try:
            pad = Pad.objects.get(slug=slug, deleted_at__isnull=True)
        except Pad.DoesNotExist:
            raise ValueError('Pad not found')
        if pad.owner != me:
            raise PermissionError('Only the owner can delete this pad')
        pad.soft_delete()
        return True
