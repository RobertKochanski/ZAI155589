import graphene
from graphene_django import DjangoObjectType

from .models import Pokemon, Type, Ability, Move
from django.contrib.auth.models import User


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


# Zapytania (queries)
class Query(graphene.ObjectType):
    pokemons = graphene.List(
        PokemonType,
        limit=graphene.Int(),
        offset=graphene.Int()
    )
    pokemon = graphene.Field(PokemonType, id=graphene.Int(required=True))

    types = graphene.List(TypeType, name=graphene.String())
    abilities = graphene.List(AbilityType)
    moves = graphene.List(MoveType)

    users = graphene.List(UserType)

    # resolvery
    def resolve_pokemons(root, info, limit, offset):
        queryset = Pokemon.objects.all()

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_pokemon(root, info, id):
        return Pokemon.objects.get(id=id)

    def resolve_types(root, info, name):
        queryset = Type.objects.all()

        if name:
            queryset = Type.objects.filter(name__startswith=name)

        return queryset

    def resolve_abilities(root, info):
        return Ability.objects.all()

    def resolve_moves(root, info):
        return Move.objects.all()

    def resolve_users(root, info):
        return User.objects.all()

    def resolve_user(root, info, id):
        return User.objects.get(id=id)


schema = graphene.Schema(query=Query)
