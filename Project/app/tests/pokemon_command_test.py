from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from app.models import Pokemon, Type, Ability, Move


class PokemonTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ash",
            password="pikachu123"
        )

        # SlugRelatedField w serializers.py blokuje tworzenie nowych rekordów Type, Ability i Move dlatego tworzymy je wcześniej,
        Type.objects.get_or_create(name="ghost")
        Type.objects.get_or_create(name="poison")

        Ability.objects.get_or_create(name="cursed-body")

        Move.objects.get_or_create(name="shadow-ball")
        Move.objects.get_or_create(name="dark-pulse")

        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def test_CreatePokemon_WithCorrectData_ReturnCreated(self):
        # Arrange
        url = reverse("pokemon-list")

        data = {
            "name": "gengar",
            "height": 15,
            "weight": 405,
            "types": ["ghost", "poison"],
            "abilities": ["cursed-body"],
            "moves": ["shadow-ball", "dark-pulse"],
            "sprite": ""
        }

        # Act
        response = self.client.post(url, data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Pokemon.objects.count() == 1

        pokemon = Pokemon.objects.get(name="gengar")

        assert pokemon.height == 15
        assert pokemon.weight == 405


    def test_CreatePokemon_WithManyWrongData_ReturnBadRequest(self):
        # Arrange
        url = reverse("pokemon-list")

        data = {
            "name": "invalidmon",
            "height": -15,
            "weight": -405
        }

        # Act
        response = self.client.post(url, data, format="json")

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data["message"]) == 5
        assert response.data["error"] is True
        assert response.data["message"]["height"][0] == "Height must be positive"
        assert response.data["message"]["weight"][0] == "Weight must be positive"
        assert response.data["message"]["types"][0] == "This field is required."
        assert response.data["message"]["abilities"][0] == "This field is required."
        assert response.data["message"]["moves"][0] == "This field is required."
        assert Pokemon.objects.count() == 0


    def test_CreatePokemon_WithNonExistType_ReturnBadRequest(self):
        # Arrange
        url = reverse("pokemon-list")

        data = {
            "name": "marshadow",
            "height": 7,
            "weight": 222,
            "types": ["fighting", "dark"],
            "abilities": ["cursed-body"],
            "moves": ["shadow-ball", "dark-pulse"]
        }

        # Act
        response = self.client.post(url, data, format="json")

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["message"]["types"][0]) == "Object with name=fighting does not exist."


    def test_PATCHPokemon_WithCorrectData_ReturnOK(self):
        # Arrange
        pokemon = Pokemon.objects.create(
            name="gengar",
            height=15,
            weight=405,
            owner=self.user
        )

        url = reverse("pokemon-detail", kwargs={"pk": pokemon.id})

        data = {
            "height": 10
        }

        # Act
        response = self.client.patch(url, data, format="json")
        pokemon.refresh_from_db()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert Pokemon.objects.count() == 1
        assert pokemon.height == 10
        assert pokemon.weight == 405


    def test_PATCHPokemon_WithoutCredentials_ReturnUnauthorized(self):
        # Arrange
        pokemon = Pokemon.objects.create(
            name="gengar",
            height=15,
            weight=405,
            owner=self.user
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"")

        url = reverse("pokemon-detail", kwargs={"pk": pokemon.id})

        data = {
            "height": 10
        }

        # Act
        response = self.client.patch(url, data, format="json")
        pokemon.refresh_from_db()

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_DELETEPokemon_WithExistPokemon_ReturnNoContent(self):
        # Arrange
        pokemon = Pokemon.objects.create(
            name="gengar",
            height=15,
            weight=405,
            owner=self.user
        )

        url = reverse("pokemon-detail", kwargs={"pk": pokemon.id})

        # Act
        response = self.client.delete(url, format="json")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT


    def test_DELETEPokemon_WithExistPokemon_ReturnUnauthorized(self):
        # Arrange
        pokemon = Pokemon.objects.create(
            name="gengar",
            height=15,
            weight=405,
            owner=self.user
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"")

        url = reverse("pokemon-detail", kwargs={"pk": pokemon.id})

        # Act
        response = self.client.delete(url, format="json")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED