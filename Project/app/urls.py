from django.urls import path

from app.views import PokemonListCreateView, PokemonDetailView, PokemonSummaryView, MeView, RegisterView, TypesView, \
    CustomTokenRefreshView, CustomTokenObtainPairView, LogoutView
from . import views

urlpatterns = [
    path("pokemons/", PokemonListCreateView.as_view(), name=views.PokemonListCreateView.name),
    path("pokemons/<int:pk>/", PokemonDetailView.as_view(), name=PokemonDetailView.name),
    path("pokemons/summary/", PokemonSummaryView.as_view(), name=PokemonSummaryView.name),
    path("user/", MeView.as_view(), name=views.MeView.name),
    path("register/", RegisterView.as_view(), name=views.RegisterView.name),
    path("types/", TypesView.as_view(), name=views.TypesView.name),

    # TOKEN
    path("token/", CustomTokenObtainPairView.as_view(), name=views.CustomTokenObtainPairView.name),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name=views.CustomTokenRefreshView.name),
    path("logout/", LogoutView.as_view(), name=views.LogoutView.name),
]
