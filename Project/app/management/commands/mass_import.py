from django.core.management.base import BaseCommand

from app.management.services import import_pokemons


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        import_pokemons(151)

        self.stdout.write("Pokemons imported successfully")
