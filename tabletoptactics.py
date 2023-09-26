import dataclasses
import datetime
import urllib.parse

@dataclasses.dataclass
class ArmyInfo:
    faction_id: int
    faction: str
    player_id: int = None
    subfaction_id: int = None

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
