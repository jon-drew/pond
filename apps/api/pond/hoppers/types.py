import strawberry
import strawberry_django
from strawberry import auto
from strawberry.types import Info

from pond.hoppers import models


@strawberry_django.type(models.Hopper)
class HopperType:
    id: auto
    username: auto
    email: auto
    name: auto
    anonymous: auto
    slug: auto
    created_at: auto

    @strawberry.field
    def is_followed_by_me(self, info: Info) -> bool:
        from django.conf import settings
        from pond.hoppers.tokens import decode_access_token
        import jwt
        token = info.context.request.COOKIES.get(settings.ACCESS_TOKEN_COOKIE)
        if not token:
            return False
        try:
            payload = decode_access_token(token)
        except jwt.InvalidTokenError:
            return False
        return models.Pair.objects.filter(
            first_hopper_id=payload['sub'], second_hopper=self
        ).exists()


@strawberry_django.type(models.Pair)
class PairType:
    id: auto
    first_hopper: HopperType
    second_hopper: HopperType
