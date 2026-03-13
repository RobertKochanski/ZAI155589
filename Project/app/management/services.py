import asyncio

import httpx

from app.models import Pokemon, Type, Ability, Move


async def fetch_pokemon_list(limit=20):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    data = response.json()
    return data["results"]


async def fetch_pokemon_details(client, url, semaphore):
    async with semaphore:
        response = await client.get(url)
        return response.json()


async def fetch_all_pokemons(limit=20):
    pokemons = await fetch_pokemon_list(limit)
    semaphore = asyncio.Semaphore(10)

    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [
            fetch_pokemon_details(client, p["url"], semaphore)
            for p in pokemons
        ]

        results = await asyncio.gather(*tasks)

    return results


def import_pokemons(limit=20):
    results = asyncio.run(fetch_all_pokemons(limit))

    pokemon_objs = []
    type_names = set()
    ability_names = set()
    move_names = set()

    # zbieranie danych
    for data in results:
        pokemon_objs.append(
            Pokemon(
                name=data["name"],
                height=data["height"],
                weight=data["weight"]
            )
        )

        type_names |= {t["type"]["name"] for t in data["types"]}
        ability_names |= {a["ability"]["name"] for a in data["abilities"]}
        move_names |= {m["move"]["name"] for m in data["moves"][:10]}


    with transaction.atomic():

        # bulk create słowników
        Type.objects.bulk_create(
            [Type(name=n) for n in type_names],
            ignore_conflicts=True
        )

        Ability.objects.bulk_create(
            [Ability(name=n) for n in ability_names],
            ignore_conflicts=True
        )

        Move.objects.bulk_create(
            [Move(name=n) for n in move_names],
            ignore_conflicts=True
        )

        # bulk create pokemonów
        Pokemon.objects.bulk_create(pokemon_objs, ignore_conflicts=True)

        # mapy obiektów
        pokemon_map = {p.name: p for p in Pokemon.objects.all()}
        type_map = {t.name: t for t in Type.objects.all()}
        ability_map = {a.name: a for a in Ability.objects.all()}
        move_map = {m.name: m for m in Move.objects.all()}

        pokemon_types = []
        pokemon_abilities = []
        pokemon_moves = []

        # relacje
        for data in results:

            p = pokemon_map[data["name"]]

            for t in data["types"]:
                pokemon_types.append(
                    Pokemon.types.through(
                        pokemon_id=p.id,
                        type_id=type_map[t["type"]["name"]].id
                    )
                )

            for a in data["abilities"]:
                pokemon_abilities.append(
                    Pokemon.abilities.through(
                        pokemon_id=p.id,
                        ability_id=ability_map[a["ability"]["name"]].id
                    )
                )

            for m in data["moves"][:10]:
                pokemon_moves.append(
                    Pokemon.moves.through(
                        pokemon_id=p.id,
                        move_id=move_map[m["move"]["name"]].id
                    )
                )

        Pokemon.types.through.objects.bulk_create(pokemon_types, ignore_conflicts=True)
        Pokemon.abilities.through.objects.bulk_create(pokemon_abilities, ignore_conflicts=True)
        Pokemon.moves.through.objects.bulk_create(pokemon_moves, ignore_conflicts=True)
