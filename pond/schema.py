import graphene

from graphene import ObjectType, Node, Schema
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType

from hoppers.models import Hopper
from pads.models import Pad
from events.models import Event
from ribbits.models import Ribbit

class HopperNode(DjangoObjectType):
    class Meta:
        model = Hopper
        interfaces = (Node, )

class PadNode(DjangoObjectType):
    class Meta:
        model = Pad
        interfaces = (Node, )

class EventNode(DjangoObjectType):
    class Meta:
        model = Event
        interfaces = (Node, )

class RibbitNode(DjangoObjectType):
    class Meta:
        model = Ribbit
        interfaces = (Node, )

class Query(ObjectType):
    hopper = Node.Field(HopperNode)
    all_hoppers = DjangoConnectionField(HopperNode)

    pad = Node.Field(PadNode)
    all_pads = DjangoConnectionField(PadNode)

    event = Node.Field(EventNode)
    all_events = DjangoConnectionField(EventNode)

    ribbit = Node.Field(RibbitNode)
    all_ribbits = DjangoConnectionField(RibbitNode)

schema = Schema(query=Query)


# from graphene import ObjectType, Node, Schema
# from graphene_django.fields import DjangoConnectionField
# from graphene_django.types import DjangoObjectType

# class CategoryNode(DjangoObjectType):

#     class Meta:
#         model = Category
#         interfaces = (Node, )

# class IngredientNode(DjangoObjectType):

#     class Meta:
#         model = Ingredient
#         interfaces = (Node, )

# class Query(ObjectType):
#     category = Node.Field(CategoryNode)
#     all_categories = DjangoConnectionField(CategoryNode)

#     ingredient = Node.Field(IngredientNode)
#     all_ingredients = DjangoConnectionField(IngredientNode)

# schema = Schema(query=Query)