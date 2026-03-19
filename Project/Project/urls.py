"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
from rest_framework import permissions

from app.views import PokemonListView, PokemonView, PokemonCreateView, PokemonUpdateView, PokemonDeleteView

schema_view = get_schema_view(
    openapi.Info(
        title='POKEGGER',
        default_version='v1',
        description='API ZAI endpoints',
        terms_of_service='https://www.google.com/policies/terms/',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # SWAGGER (Project2)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # APP (Project2)
    path("api/", include("app.urls")),

    # GRAPHQL (Project2)
    path("graphql/", GraphQLView.as_view(graphiql=True)),

    # BOOTSTRAP (Project1)
    path("", PokemonListView.as_view(), name="pokemon-list"),
    path("<int:pk>/", PokemonView.as_view(), name="pokemon-detail"),
    path("create/", PokemonCreateView.as_view(), name="pokemon-create"),
    path("edit/<int:pk>/", PokemonUpdateView.as_view(), name="pokemon-update"),
    path("delete/<int:pk>/", PokemonDeleteView.as_view(), name="pokemon-delete"),
]
