from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status


from .customPermissions import IsOwnerOrAdmin
from .models import Pokemon, Type
from .serializers import PokemonWriteSerializer, PokemonReadSerializer, RegisterSerializer, UserSerializer, \
    PokemonSummarySerializer, TypeSerializer, LogoutSerializer


class PokemonListCreateView(generics.ListCreateAPIView):
    name = 'pokemon-list'
    queryset = Pokemon.objects.prefetch_related(
        "types",
        "abilities",
        "moves"
    )
    permission_classes = [IsAuthenticated]
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
    search_fields = ["name"]
    ordering_fields = [
        "name",
        "height",
        "weight"
    ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PokemonWriteSerializer
        return PokemonReadSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PokemonDetailView(generics.RetrieveUpdateDestroyAPIView):
    name = "pokemon-detail"
    queryset = Pokemon.objects.prefetch_related(
        "types",
        "abilities",
        "moves"
    )
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PokemonWriteSerializer
        return PokemonReadSerializer


class PokemonSummaryView(generics.ListAPIView):
    name = "pokemon-summary"
    queryset = Pokemon.objects.prefetch_related(
        "types",
        "abilities",
        "moves"
    )
    serializer_class = PokemonSummarySerializer
    permission_classes = [IsAuthenticated]
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
    search_fields = ["name"]
    ordering_fields = [
        "name",
        "height",
        "weight"
    ]


class TypesView(generics.ListAPIView):
    name = "allTypes"
    permission_classes = [IsAuthenticated]
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    search_fields = ["name"]
    ordering_fields = ["name"]


class RegisterView(generics.CreateAPIView):
    name = "register"
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MeView(generics.RetrieveAPIView):
    name = "user"
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    name = "token"

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    name = "refresh token"

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(generics.CreateAPIView):
    name = "logout"
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_205_RESET_CONTENT)