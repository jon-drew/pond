import strawberry
from strawberry.extensions import QueryDepthLimiter

from pond.hoppers.queries import HopperQueries
from pond.hoppers.mutations import HopperMutations, AuthPayload
from pond.pads.queries import PadQueries
from pond.pads.mutations import PadMutations
from pond.events.queries import EventQueries
from pond.events.mutations import EventMutations
from pond.ribbits.queries import RibbitQueries
from pond.ribbits.mutations import RibbitMutations


@strawberry.type
class Query(HopperQueries, PadQueries, EventQueries, RibbitQueries):
    pass


@strawberry.type
class Mutation(HopperMutations, PadMutations, EventMutations, RibbitMutations):
    pass


def _build_schema():
    from django.conf import settings
    allow_introspection = getattr(settings, 'GRAPHQL_INTROSPECTION', True)
    return strawberry.Schema(
        query=Query,
        mutation=Mutation,
        extensions=[QueryDepthLimiter(max_depth=10)],
        introspection=allow_introspection,
    )


schema = _build_schema()
