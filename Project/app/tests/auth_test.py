from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class AuthTests(APITestCase):
    def test_UserRegistration_WithCorrectData_ReturnCreated(self):
        # Arrange
        client = APIClient()

        url = reverse("register")

        data = {
            "username": "ash",
            "password": "pikachu123",
            "email": "ash@test.com"
        }

        # Act
        response = client.post(url, data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "ash"


    def test_GetTokenAndUser_WithCorrectData_SetCredentialsAndReturnOK(self):
        # Arrange
        client = APIClient()

        getTokenUrl = reverse("token")
        getUserUrl = reverse("user")
        user = User.objects.create_user('admin', 'admin@admin.com', 'admin123')

        # Act
        responseToken = client.post(getTokenUrl, {"username": "admin", "password": "admin123"}, format="json")
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {responseToken.data['access']}")

        response = client.get(getUserUrl)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user.username


    def test_UserRegistration_WithWrongData_ReturnBadRequest(self):
        # Arrange
        client = APIClient()

        url = reverse("register")

        data = {
            "username": "ash",
            "email": "ash@test.com"
        }

        # Act
        response = client.post(url, data, format="json")

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_GetToken_WithWrongData_ReturnUnauthorized(self):
        # Arrange
        client = APIClient()

        getTokenUrl = reverse("token")

        # Act
        responseToken = client.post(getTokenUrl, {"username": "admin", "password": "admin"}, format="json")

        # Assert
        assert responseToken.status_code == status.HTTP_401_UNAUTHORIZED