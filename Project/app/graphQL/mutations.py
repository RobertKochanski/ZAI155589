import graphene
import graphql_jwt
from graphql import GraphQLError

from app.graphQL.permissions import check_owner_or_admin, get_authenticated_user
from app.graphQL.types import PokemonType
from app.models import Pokemon, Move, Ability, Type


class CreatePokemon(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        height = graphene.Int(required=True)
        weight = graphene.Int(required=True)

        type_ids = graphene.List(graphene.Int)
        ability_ids = graphene.List(graphene.Int)
        move_ids = graphene.List(graphene.Int)

    pokemon = graphene.Field(PokemonType)

    def mutate(self, info, name, height, weight,
               type_ids=None, ability_ids=None, move_ids=None):

        if len(type_ids) > 2:
            raise GraphQLError("Pokemon cannot have more than 2 types.")
        if type_ids is None or len(type_ids) == 0:
            raise GraphQLError("Pokemon cannot have no types.")
        if ability_ids is None or len(ability_ids) == 0:
            raise GraphQLError("Pokemon cannot have no abilities.")
        if move_ids is None or len(move_ids) == 0:
            raise GraphQLError("Pokemon cannot have no moves.")

        user = get_authenticated_user(info)

        pokemon = Pokemon.objects.create(
            name=name,
            height=height,
            weight=weight,
            owner=user
        )

        if type_ids:
            pokemon.types.set(Type.objects.filter(id__in=type_ids))

        if ability_ids:
            pokemon.abilities.set(Ability.objects.filter(id__in=ability_ids))

        if move_ids:
            pokemon.moves.set(Move.objects.filter(id__in=move_ids))

        return CreatePokemon(pokemon=pokemon)


class UpdatePokemon(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

        name = graphene.String()
        height = graphene.Int()
        weight = graphene.Int()

        type_ids = graphene.List(graphene.Int)
        ability_ids = graphene.List(graphene.Int)
        move_ids = graphene.List(graphene.Int)

    pokemon = graphene.Field(PokemonType)

    def mutate(self, info, id, **kwargs):
        user = get_authenticated_user(info)

        pokemon = Pokemon.objects.get(id=id)

        check_owner_or_admin(user, pokemon)

        # pola proste
        for field in ["name", "height", "weight"]:
            if field in kwargs:
                setattr(pokemon, field, kwargs[field])

        pokemon.save()

        # relacje
        if "type_ids" in kwargs:
            pokemon.types.set(Type.objects.filter(id__in=kwargs["type_ids"]))

        if "ability_ids" in kwargs:
            pokemon.abilities.set(Ability.objects.filter(id__in=kwargs["ability_ids"]))

        if "move_ids" in kwargs:
            pokemon.moves.set(Move.objects.filter(id__in=kwargs["move_ids"]))

        return UpdatePokemon(pokemon=pokemon)


class DeletePokemon(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        user = get_authenticated_user(info)

        pokemon = Pokemon.objects.get(id=id)

        check_owner_or_admin(user, pokemon)

        pokemon.delete()

        return DeletePokemon(ok=True)


class Mutation(graphene.ObjectType):
    # JWT
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_pokemon = CreatePokemon.Field()
    update_pokemon = UpdatePokemon.Field()
    delete_pokemon = DeletePokemon.Field()