from graphql import GraphQLError


def get_authenticated_user(info):
    user = info.context.user
    if not user or not user.is_authenticated:
        raise GraphQLError("Authentication required")
    return user


def check_owner_or_admin(user, pokemon):
    if pokemon.owner != user and not user.is_superuser:
        raise GraphQLError("Not permitted")