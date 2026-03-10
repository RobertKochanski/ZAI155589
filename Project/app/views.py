from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .customPermissions import IsOwnerOrAdmin
from .models import Pokemon
from .serializers import PokemonWriteSerializer, PokemonReadSerializer, RegisterSerializer, UserSerializer, \
    PokemonSummarySerializer


class PokemonViewSet(viewsets.ModelViewSet):
    name = "pokemon"
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    queryset = Pokemon.objects.prefetch_related(
        "types",
        "abilities",
        "moves"
    )

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = {
        "height": ["exact", "gt", "lt"],
        "weight": ["exact", "gt", "lt"],
        "types__name": ["exact"]
    }
    search_fields = [
        "name"
    ]
    ordering_fields = [
        "name",
        "height",
        "weight"
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PokemonWriteSerializer

        return PokemonReadSerializer

    @action(detail=False, methods=["get"])
    def summary(self, request):
        pokemons = self.get_queryset()

        page = self.paginate_queryset(pokemons)
        if page is not None:
            serializer = PokemonSummarySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PokemonSummarySerializer(pokemons, many=True)

        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    name = "register"
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MeView(APIView):
    name = "user"
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    @swagger_auto_schema(tags=["Auth"])
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    name = "token"
    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)