from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import PokemonViewSet, MeView, RegisterView

router = DefaultRouter()
router.register("pokemons", PokemonViewSet)

urlpatterns = router.urls + [
    path("user/", MeView.as_view(), name=views.MeView.name),
    path("register/", RegisterView.as_view(), name=views.RegisterView.name),
]