import dataclasses
import datetime
import urllib.parse

@dataclasses.dataclass
class ArmyInfo:
    faction_id: int
    faction: str
    player_id: int = None
    subfaction_id: int = None
    edition: int = None
    winner: bool = None

@dataclasses.dataclass
class ShowData:
    release_date: datetime.date
    slug: str
    youtube_slug: str

    game_id: int
    showtype_id: int
    servoskull_id: int

    army1: ArmyInfo
    army2: ArmyInfo

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

def _get_id_from_slug(slug, lookup, missing_value):
    for obj, obj_id in lookup.items():
        if normalize_for_slug(obj) in slug:
            return obj_id, obj

    return lookup[missing_value], missing_value

def get_game(slug, games, missing_value):
    if 'warhammer-40k' in slug:
        return games['Warhammer 40,000'], 'Warhammer 40,000'

    return _get_id_from_slug(slug, games, missing_value)

def get_showtype(slug, showtypes, missing_value):
    showtype_id, _ = _get_id_from_slug(slug, showtypes, missing_value)
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
        if subfaction in factions:
            # Occurs for "World Eaters" where we want to match the faction not the subfaction
            # and "Slaves to Darkness" where we want to match the AoS faction not the Chaos Space Marines detachment
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

def update_army_info(army, input_data, army_number, players, factions, subfactions):
    prefix = f'army{army_number}'
    player = getattr(input_data, prefix + 'player')

    if army:
        army.player_id = players[player]
    else:
        if player:
            faction = getattr(input_data, prefix + 'faction')
            army = ArmyInfo(faction_id=factions[faction], faction=faction, player_id=players[player])
        else:  
            return None

    subfaction = getattr(input_data, prefix + 'subfaction')
    if subfaction:
        army.subfaction_id = subfactions[subfaction][0]

    return army

def set_winner(army1, army2, input_data, players):
    if input_data.winner:
        winner_id = players[input_data.winner]
        army1.winner = army1.player_id == winner_id
        army2.winner = army2.player_id == winner_id

def create_show_data(input_data, games, showtypes, players, factions, subfactions):
    release_date, slug = parse_url(input_data.url)

    game_id, game = get_game(slug, games, input_data.game)
    showtype_id = get_showtype(slug, showtypes, input_data.showtype)
    servoskull = input_data.servoskull
    servoskull_id = players[servoskull] if servoskull else None

    army1, army2 = extract_armies_from_slug(slug, factions, subfactions)

    army1 = update_army_info(army1, input_data, 1, players, factions, subfactions)
    army2 = update_army_info(army2, input_data, 2, players, factions, subfactions)

    set_winner(army1, army2, input_data, players)

    army1.edition = get_edition(army1, game, release_date)
    if army2:
        army2.edition = get_edition(army2, game, release_date)

    return ShowData(release_date, slug, input_data.youtube, game_id, showtype_id, servoskull_id, army1, army2)
