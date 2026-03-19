from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from app.models import Pokemon, Type, Ability, Move

# GraphQL typy oparte o modele Django
class PokemonType(DjangoObjectType):
    class Meta:
        model = Pokemon
        fields = "__all__"


class TypeType(DjangoObjectType):
    class Meta:
        model = Type
        fields = "__all__"


class AbilityType(DjangoObjectType):
    class Meta:
        model = Ability
        fields = "__all__"


class MoveType(DjangoObjectType):
    class Meta:
        model = Move
        fields = "__all__"


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"
