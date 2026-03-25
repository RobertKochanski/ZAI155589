from django.core.management.base import BaseCommand

from app.management.services import import_pokemons


class Command(BaseCommand):
    help = "Import pokemons"

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=151,
            help='Pokemons to import.'
        )

        parser.add_argument(
            '--offset',
            type=int,
            default=0,
            help='Pokemons to skip.'
        )

    def handle(self, *args, **kwargs):
        limit = kwargs['limit']
        offset = kwargs['offset']

        import_pokemons(limit, offset)

        self.stdout.write("Pokemons imported successfully")
