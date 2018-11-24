import graphene
import graphql_jwt

from graphene import ObjectType, Node, Schema
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model

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

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class Query(ObjectType):
    hopper = graphene.Field(HopperType,id=graphene.Int())
    all_hoppers = graphene.List(HopperType)

    pad = graphene.Field(PadType,id=graphene.Int())
    all_pads = graphene.List(PadType)

    event = graphene.Field(EventType,id=graphene.Int())
    all_events = graphene.List(EventType)

    ribbit = graphene.Field(RibbitType,id=graphene.Int())
    all_ribbits = graphene.List(RibbitType)

    def resolve_hopper(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            hopper_object = Hopper.objects.get(pk=id)
            if hopper_object.anonymous != True:
                return Hopper.objects.get(pk=id)
        return None

    def resolve_all_hoppers(self, info, **kwargs):
        return Hopper.objects.exclude(anonymous=True)

    def resolve_pad(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Pad.objects.get(pk=id)
        return None

    def resolve_all_pads(self, info, **kwargs):
        return Pad.objects.all()

    def resolve_event(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Event.objects.get(pk=id)
        return None

    def resolve_all_events(self, info, **kwargs):
        return Event.objects.all()

    def resolve_ribbit(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Ribbit.objects.get(pk=id)
        return None

    def resolve_all_ribbits(self, info, **kwargs):
        return Ribbit.objects.all()

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = Schema(query=Query, mutation=Mutation)