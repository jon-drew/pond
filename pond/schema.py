import graphene

from graphene import ObjectType, Node, Schema
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType

from hoppers.models import Hopper
from pads.models import Pad
from events.models import Event
from ribbits.models import Ribbit

class HopperType(DjangoObjectType):
    class Meta:
        model = Hopper

class PadType(DjangoObjectType):
    class Meta:
        model = Pad

class EventType(DjangoObjectType):
    class Meta:
        model = Event

class RibbitType(DjangoObjectType):
    class Meta:
        model = Ribbit

class Query(ObjectType):
    hopper = graphene.Field(HopperType,id=graphene.Int())
    all_hoppers = graphene.List(HopperType)

    pad = graphene.Field(PadType,id=graphene.Int())
    all_pads = graphene.List(PadType)

    event = graphene.Field(EventType,id=graphene.Int())
    all_events = graphene.List(EventType)

    ribbit = graphene.Field(RibbitType,id=graphene.Int())
    all_ribbits = graphene.List(RibbitType)

    def resolve_hopper(self, *args, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Hopper.objects.get(pk=id)
        return None

    def resolve_all_hoppers(self, args):
        return Hopper.objects.all()

    def resolve_pad(self, args):
        id = kwargs.get('id')
        if id is not None:
            return Pad.objects.get(pk=id)
        return None

    def resolve_all_pads(self, *args, **kwargs):
        return Pad.objects.all()

    def resolve_event(self, args):
        id = kwargs.get('id')
        if id is not None:
            return Event.objects.get(pk=id)
        return None

    def resolve_all_events(self, *args, **kwargs):
        return Event.objects.all()

    def resolve_ribbit(self, args):
        id = kwargs.get('id')
        if id is not None:
            return Ribbit.objects.get(pk=id)
        return None

    def resolve_all_ribbits(self, *args, **kwargs):
        return Ribbit.objects.all()

schema = Schema(query=Query)