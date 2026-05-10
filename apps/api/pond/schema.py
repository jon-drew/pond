import strawberry

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


schema = strawberry.Schema(query=Query, mutation=Mutation)
