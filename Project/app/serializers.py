from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from app.exceptions import PokemonTypeLimitExceeded, PokemonTypeDuplicated, PokemonMoveDuplicated
from .models import Pokemon, Type, Ability, Move


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = "__all__"


class PokemonReadSerializer(serializers.ModelSerializer):
    types = TypeSerializer(many=True)
    abilities = AbilitySerializer(many=True)
    moves = MoveSerializer(many=True)

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Pokemon
        fields = "__all__"


class PokemonSummarySerializer(serializers.ModelSerializer):
    types = TypeSerializer(many=True)

    class Meta:
        model = Pokemon
        fields = ["name", "height", "weight", "types"]


class PokemonWriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        error_messages={
            "required": "Pokemon name is required",
            "blank": "Pokemon name cannot be empty"
        }
    )

    height = serializers.IntegerField(
        error_messages={
            "required": "Height is required",
            "invalid": "Height must be a number"
        }
    )

    weight = serializers.IntegerField(
        error_messages={
            "required": "Weight is required",
            "invalid": "Weight must be a number"
        }
    )

    types = serializers.SlugRelatedField(
        many=True,
        queryset=Type.objects.all(),
        slug_field="name"
    )

    abilities = serializers.SlugRelatedField(
        many=True,
        queryset=Ability.objects.all(),
        slug_field="name"
    )

    moves = serializers.SlugRelatedField(
        many=True,
        queryset=Move.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Pokemon
        fields = [
            "name",
            "height",
            "weight",
            "types",
            "abilities",
            "moves",
        ]

    def validate_name(self, value):
        if Pokemon.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(
                "Pokemon with this name already exists"
            )

        return value.lower()

    def validate_height(self, value):
        if value <= 0:
            raise serializers.ValidationError("Height must be positive")
        return value

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be positive")
        return value

    def validate_types(self, value):
        if len(value) > 2:
            raise PokemonTypeLimitExceeded()

        names = [t.name for t in value]

        if len(names) != len(set(names)):
            raise PokemonTypeDuplicated()

        return value

    def validate_moves(self, value):
        names = [t.name for t in value]

        if len(names) != len(set(names)):
            raise PokemonMoveDuplicated()

        return value

    def validate_abilities(self, value):
        names = [t.name for t in value]

        if len(names) != len(set(names)):
            raise PokemonAbilitiesDuplicated()

        return value


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self, **kwargs):
        refresh_token = self.validated_data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()