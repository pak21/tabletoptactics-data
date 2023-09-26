import dataclasses
import datetime
import urllib.parse

@dataclasses.dataclass
class ArmyInfo:
    faction_id: int
    faction: str
    player_id: int = None
    subfaction_id: int = None

@dataclasses.dataclass
class InputData:
    url: str = None
    youtube: str = None
    game: str = None
    showtype: str = None
    winner: str = None
    servoskull: str = None

    army1player: str = None
    army1faction: str = None
    army1subfaction: str = None

    army2player: str = None
    army2faction: str = None
    army2subfaction: str = None

def parse_url(raw_url):
    url = urllib.parse.urlparse(raw_url)
    components = url.path.split('/')
    date_components = [int(c) for c in components[1:4]]
    return datetime.date(*date_components), components[4]

def normalize_for_slug(s):
    return s.lower().replace(' ', '-').replace(',', '').replace('é', 'e').replace("'", '')

def _get_id_from_slug(slug, lookup, missing_fn):
    for obj, obj_id in lookup.items():
        if normalize_for_slug(obj) in slug:
            return obj_id, obj

    obj = missing_fn()
    return lookup[obj], obj

def get_game(slug, games, missing_fn):
    if 'warhammer-40k' in slug:
        return games['Warhammer 40,000'], 'Warhammer 40,000'

    return _get_id_from_slug(slug, games, missing_fn)

def get_showtype(slug, showtypes, missing_fn):
    showtype_id, _ = _get_id_from_slug(slug, showtypes, missing_fn)
    return showtype_id

def extract_armies_from_slug(slug, factions, subfactions):
    armies_found = {}

    for faction, faction_id in factions.items():
        faction_index = slug.find(normalize_for_slug(faction))
        if faction_index != -1:
            # If we found 'chaos-space-marines', we don't want to match this as a Space Marines army
            if faction == 'Space Marines' and faction_index >= 6 and slug[faction_index-6:faction_index] == 'chaos-':
                pass
            else:
                armies_found[faction_index] = ArmyInfo(faction_id=faction_id, faction=faction)

    for subfaction, (subfaction_id, faction, faction_id) in subfactions.items():
        if subfaction == 'World Eaters':
            # This causes problems because it is also the name of the faction
            continue
        subfaction_index = slug.find(normalize_for_slug(subfaction))
        if subfaction_index != -1:
            armies_found[subfaction_index] = ArmyInfo(faction_id=faction_id, faction=faction, subfaction_id=subfaction_id)

    match len(armies_found):
        case 0:
            raise Exception(f'Found no armies in slug "{slug}"; giving up')

        case 1:
            idx = list(armies_found)[0]
            return [armies_found[idx], None]

        case 2:
            return [armies_found[k] for k in sorted(armies_found)]

        case _:
            raise Exception(f'Found {len(armies_found)} armies in slug "{slug}"; giving up')

FACTION_DATES_9TH = {
    'Aeldari': datetime.date(2022, 2, 26),
    'Harlequins': datetime.date(2022, 2, 26),
    'Tyranids': datetime.date(2022, 4, 9),
    'Chaos Knights': datetime.date(2022, 5, 7),
    'Imperial Knights': datetime.date(2022, 5, 10),
    'Chaos Space Marines': datetime.date(2022, 6, 25),
    'Chaos Daemons': datetime.date(2022, 8, 27),
    'Leagues of Votann': datetime.date(2022, 9, 17), # Included for reference, but can't be any games before this!
    'Astra Militarum': datetime.date(2022, 11, 12),
    'World Eaters': datetime.date(2023, 2, 4),
}

def _get_edition_wh40k(army, release_date):
    # Last 9th Edition game on the channel was 2023-05-30
    if release_date > datetime.date(2023, 5, 30):
        return 10

    try:
        is_8th = release_date < FACTION_DATES_9TH[army.faction]
    except KeyError:
        is_8th = False

    return 8 if is_8th else 9

_EDITION_FUNCTIONS = {
    'Warhammer 40,000': _get_edition_wh40k,
    'Age of Sigmar': lambda a, rd: 3
}

def get_edition(army, game, release_date):
    return _EDITION_FUNCTIONS[game](army, release_date)

def parse_input(data):
    input_data = InputData()
    for line in data.split('\n'):
        if not line:
            continue
        key, value = line.split(': ', 1)
        if not hasattr(input_data, key):
            raise Exception(f'Unknown input data key {key}')
        setattr(input_data, key, value)

    return input_data
