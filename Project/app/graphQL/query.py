import graphene
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from app.graphQL.types import PokemonType, TypeType, AbilityType, MoveType, UserType
from app.models import Pokemon, Type, Ability, Move


# Zapytania (queries)
class Query(graphene.ObjectType):
    pokemons = graphene.List(
        PokemonType,
        limit=graphene.Int(),
        offset=graphene.Int()
    )
    pokemon = graphene.Field(PokemonType, id=graphene.Int(required=True))
    pokemon_by_name = graphene.List(PokemonType, name=graphene.String())


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
        return get_object_or_404(Pokemon, pk=id)

    def resolve_pokemon_by_name(root, info, name):
        queryset = Pokemon.objects.all()

        if name:
            queryset = Pokemon.objects.filter(name__startswith=name)

        return queryset

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
        return get_object_or_404(User, pk=id)