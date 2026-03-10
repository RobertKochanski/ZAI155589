import httpx
import asyncio

from app.models import Pokemon, Type, Ability, Move

async def fetch_pokemon_list(limit=20):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    data = response.json()
    return data["results"]


async def fetch_pokemon_details(client, url):
    response = await client.get(url)

    return response.json()


async def fetch_all_pokemons(limit=20):
    pokemons = await fetch_pokemon_list(limit)

    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_pokemon_details(client, p["url"])
            for p in pokemons
        ]

        results = await asyncio.gather(*tasks)

    return results


def save_pokemons(results):
    for data in results:
        pokemon, _ = Pokemon.objects.get_or_create(
            name=data["name"],
            defaults={
                "height": data["height"],
                "weight": data["weight"],
            }
        )

        for t in data["types"]:
            type_obj, _ = Type.objects.get_or_create(
                name=t["type"]["name"]
            )

            pokemon.types.add(type_obj)

        for a in data["abilities"]:
            ability_obj, _ = Ability.objects.get_or_create(
                name=a["ability"]["name"]
            )

            pokemon.abilities.add(ability_obj)

        for m in data["moves"][:10]:
            move_obj, _ = Move.objects.get_or_create(
                name=m["move"]["name"]
            )

            pokemon.moves.add(move_obj)


def import_pokemons(limit=20):
    results = asyncio.run(fetch_all_pokemons(limit))
    save_pokemons(results)