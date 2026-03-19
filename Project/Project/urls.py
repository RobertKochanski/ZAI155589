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

from app import views
from app.views import pokemon_list, pokemon_detail

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

    # SWAGGER
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    # APP
    path("api/", include("app.urls")),

    # GRAPHQL
    path("graphql/", GraphQLView.as_view(graphiql=True)),

    # BOOTSTRAP
    path('', pokemon_list, name='pokemon_list'),
    path('detail/<int:pk>/', pokemon_detail, name='pokemon_detail'),
]
