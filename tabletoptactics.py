import dataclasses

@dataclasses.dataclass
class ArmyInfo:
    faction_id: int
    faction: str
    player_id: int = None
    subfaction_id: int = None

def normalize_for_slug(s):
    return s.lower().replace(' ', '-').replace(',', '').replace('é', 'e').replace("'", '')

def extract_armies_from_slug(slug, factions, subfactions):
    armies_found = {}

    for faction, faction_id in factions.items():
        faction_index = slug.find(normalize_for_slug(faction))
        if faction_index != -1:
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
