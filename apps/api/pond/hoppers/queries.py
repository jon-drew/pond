from typing import Optional

import jwt
import strawberry
from strawberry.types import Info

from pond.hoppers.models import Hopper
from pond.hoppers.types import HopperType
from pond.hoppers.tokens import decode_access_token


@strawberry.type
class HopperQueries:

    @strawberry.field
    def me(self, info: Info) -> Optional[HopperType]:
        from django.conf import settings
        token = info.context.request.COOKIES.get(settings.ACCESS_TOKEN_COOKIE)
        if not token:
            return None
        try:
            payload = decode_access_token(token)
            return Hopper.objects.get(pk=payload['sub'])
        except Exception:
            return None

    @strawberry.field
    def hoppers(self) -> list[HopperType]:
        return Hopper.objects.filter(anonymous=False)

    @strawberry.field
    def hopper(self, slug: str) -> Optional[HopperType]:
        try:
            return Hopper.objects.get(slug=slug, anonymous=False)
        except Hopper.DoesNotExist:
            return None
