from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from app.tests.pokemon_samples import create_sample_pokemons


class PokemonTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="ash",
            password="pikachu123"
        )

        pokemons = create_sample_pokemons(user)
        self.arcanine = pokemons[0]
        self.dragonite = pokemons[1]

        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def test_GetAllPokemon_ReturnOKWithList(self):
        # Arrange
        url = reverse("pokemon-list")

        # Act
        response = self.client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 6

        names = [p["name"] for p in response.data["results"]]
        assert "arcanine" in names
        assert "dragonite" in names
        assert "charizard" in names

        arcanine = next(p for p in response.data["results"] if p["name"] == "arcanine")
        assert arcanine["types"][0]["name"] == "fire"


    def test_GetPokemonById_WithCorrectId_ReturnOKWithSinglePokemon(self):
        # Arrange
        url = reverse("pokemon-detail", kwargs={"pk": self.arcanine.id})

        # Act
        response = self.client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "arcanine"
        assert response.data["types"][0]["name"] == "fire"


    def test_GetPokemonById_WithWrongId_ReturnNotFound(self):
        # Arrange
        url = reverse("pokemon-detail", kwargs={"pk": 999999})

        # Act
        response = self.client.get(url)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def test_GetPokemons_WithGreaterThan10Height_ReturnOKWithList(self):
        # Asseer
        url = reverse("pokemon-list") + "?height__gt=10"

        # Act
        response = self.client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5


    def test_GetPokemons_WithFireType_ReturnOKWithList(self):
        # Asseer
        url = reverse("pokemon-list") + "?types__name=fire"

        # Act
        response = self.client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

        names = [p["name"] for p in response.data["results"]]
        assert "arcanine" in names
        assert "charizard" in names


    def test_GetPokemons_WithoutCredentials_ReturnUnauthorized(self):
        # Arrange
        url = reverse("pokemon-list")
        self.client.credentials(HTTP_AUTHORIZATION="")

        # Act
        response = self.client.get(url)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED