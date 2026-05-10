import strawberry
import strawberry_django
from strawberry import auto

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


@strawberry_django.type(models.Pair)
class PairType:
    id: auto
    first_hopper: HopperType
    second_hopper: HopperType
