from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    return Response({
        "error": True,
        "status_code": response.status_code,
        "message": response.data
    }, status=response.status_code)


class PokemonTypeLimitExceeded(APIException):
    status_code = 400
    default_detail = "Pokemon cannot have more than 2 types."
    default_code = "pokemon_type_limit"

class PokemonTypeDuplicated(APIException):
    status_code = 400
    default_detail = "Pokemon cannot have duplicate types."
    default_code = "pokemon_type_duplicated"

class PokemonMoveDuplicated(APIException):
    status_code = 400
    default_detail = "Pokemon cannot have duplicate moves."
    default_code = "pokemon_move_duplicated"

class PokemonAbilitiesDuplicated(APIException):
    status_code = 400
    default_detail = "Pokemon cannot have duplicate abilities."
    default_code = "pokemon_ability_duplicated"