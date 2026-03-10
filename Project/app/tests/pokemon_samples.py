from app.models import Pokemon, Type, Ability, Move


def create_sample_pokemons(user):
    fire, _ = Type.objects.get_or_create(name="fire")
    water, _ = Type.objects.get_or_create(name="water")
    dragon, _ = Type.objects.get_or_create(name="dragon")
    flying, _ = Type.objects.get_or_create(name="flying")
    grass, _ = Type.objects.get_or_create(name="grass")
    electric, _ = Type.objects.get_or_create(name="electric")

    flamethrower, _ = Move.objects.get_or_create(name="flamethrower")
    thunderbolt, _ = Move.objects.get_or_create(name="thunderbolt")
    vine_whip, _ = Move.objects.get_or_create(name="vine-whip")
    dragon_claw, _ = Move.objects.get_or_create(name="dragon-claw")
    hurricane, _ = Move.objects.get_or_create(name="hurricane")
    water_gun, _ = Move.objects.get_or_create(name="water-gun")

    intimidate, _ = Ability.objects.get_or_create(name="intimidate")
    blaze, _ = Ability.objects.get_or_create(name="blaze")
    torrent, _ = Ability.objects.get_or_create(name="torrent")
    overgrow, _ = Ability.objects.get_or_create(name="overgrow")
    multiscale, _ = Ability.objects.get_or_create(name="multiscale")

    pokemons = []

    arcanine = Pokemon.objects.create(name="arcanine", height=19, weight=1550, owner=user)
    arcanine.types.add(fire)
    arcanine.abilities.add(intimidate)
    arcanine.moves.add(flamethrower)
    pokemons.append(arcanine)

    dragonite = Pokemon.objects.create(name="dragonite", height=22, weight=2100, owner=user)
    dragonite.types.add(dragon, flying)
    dragonite.abilities.add(multiscale)
    dragonite.moves.add(dragon_claw, hurricane)
    pokemons.append(dragonite)

    charizard = Pokemon.objects.create(name="charizard", height=17, weight=905, owner=user)
    charizard.types.add(fire, flying)
    charizard.abilities.add(blaze)
    charizard.moves.add(flamethrower)
    pokemons.append(charizard)

    blastoise = Pokemon.objects.create(name="blastoise", height=16, weight=855, owner=user)
    blastoise.types.add(water)
    blastoise.abilities.add(torrent)
    blastoise.moves.add(water_gun)
    pokemons.append(blastoise)

    venusaur = Pokemon.objects.create(name="venusaur", height=20, weight=1000, owner=user)
    venusaur.types.add(grass)
    venusaur.abilities.add(overgrow)
    venusaur.moves.add(vine_whip)
    pokemons.append(venusaur)

    pikachu = Pokemon.objects.create(name="pikachu", height=4, weight=60, owner=user)
    pikachu.types.add(electric)
    pikachu.moves.add(thunderbolt)
    pokemons.append(pikachu)

    return pokemons