import dataclasses
import datetime
import re
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
class CampaignInfo:
    campaign_id: int
    sequence: int

@dataclasses.dataclass
class ShowData:
    release_date: datetime.date
    slug: str
    youtube_slug: str

    game_id: int
    showtype_id: int
    servoskull_id: int

    campaign: CampaignInfo

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

    campaign: str = None
    campaignsequence: int = None

    army1player: str = None
    army1faction: str = None
    army1subfaction: str = None

    army2player: str = None
    army2faction: str = None
    army2subfaction: str = None

@dataclasses.dataclass
class FactionInfo:
    faction_id: int
    game_id: int

@dataclasses.dataclass
class SubfactionInfo:
    subfaction_id: int
    faction: str
    faction_id: int

class ShowDataBuilder:
    def __init__(self, games, showtypes, players, campaigns, factions, subfactions):
        self._games = games
        self._showtypes = showtypes
        self._players = players
        self._campaigns = campaigns
        self._factions = {f: FactionInfo(fid, gid) for fid, f, gid in factions}
        self._factions_to_games = {fid: gid for fid, _, gid in factions}
        self._subfactions = {s: SubfactionInfo(sid, f, fid) for sid, s, fid, f in subfactions}
        self._subfactions_to_factions = {sid: fid for sid, _, fid, _ in subfactions}

    def parse_url(self, raw_url):
        url = urllib.parse.urlparse(raw_url)
        components = url.path.split('/')
        date_components = [int(c) for c in components[1:4]]
        return datetime.date(*date_components), components[4]

    def normalize_for_slug(self, s):
        return s.lower().replace(' ', '-').replace(',', '').replace('é', 'e').replace("'", '')

    def _get_id_from_slug(self, slug, lookup, missing_value):
        for obj, obj_id in lookup.items():
            if self.normalize_for_slug(obj) in slug:
                return obj_id, obj

        try:
            return lookup[missing_value], missing_value
        except KeyError:
            return None, None

    def get_game(self, slug, missing_value):
        if 'warhammer-40k' in slug:
            return self._games['Warhammer 40,000'], 'Warhammer 40,000'

        game_id, game = self._get_id_from_slug(slug, self._games, missing_value)

        if game_id is None:
            raise DataException(f'No game found in slug {slug} and missing value {missing_value} invalid')

        return game_id, game

    def get_showtype(self, slug, missing_value):
        if 'crusade-report' in slug:
            return self._showtypes['Narrative report']

        showtype_id, _ = self._get_id_from_slug(slug, self._showtypes, missing_value)

        if showtype_id is None:
            raise DataException(f'No show type found in slug {slug} and missing value {missing_value} invalid')

        return showtype_id

    @staticmethod
    def _merge_army_and_player(army, player_id):
        match (army, player_id):
            case (None, None): return None
            case (None, _): return ArmyInfo(faction=None, faction_id=None, player_id=player_id)
            case (_, None): return army
            case (_, _):
                army.player_id = player_id
                return army

    def extract_armies_from_slug(self, slug):
        armies_found = {}
        players_found = {}

        for faction, faction_info in self._factions.items():
            faction_index = slug.find(self.normalize_for_slug(faction))
            if faction_index != -1:
                # If we found 'chaos-space-marines', we don't want to match this as a Space Marines army
                if faction == 'Space Marines' and faction_index >= 6 and slug[faction_index-6:faction_index] == 'chaos-':
                    pass
                else:
                    armies_found[faction_index] = ArmyInfo(faction_id=faction_info.faction_id, faction=faction)

        for subfaction, subfaction_info in self._subfactions.items():
            if subfaction in self._factions:
                # Occurs for "World Eaters" where we want to match the faction not the subfaction
                # and "Slaves to Darkness" where we want to match the AoS faction not the Chaos Space Marines detachment
                continue
            subfaction_index = slug.find(self.normalize_for_slug(subfaction))
            if subfaction_index != -1:
                armies_found[subfaction_index] = ArmyInfo(faction_id=subfaction_info.faction_id, faction=subfaction_info.faction, subfaction_id=subfaction_info.subfaction_id)

        if len(armies_found) > 2:
            raise DataException(f'Found {len(armies_found)} armies in slug "{slug}"; giving up')

        for player, player_id in self._players.items():
            player_index = slug.find(self.normalize_for_slug(player))
            if player_index != -1:
                players_found[player_index] = player_id

        if len(players_found) > 2:
            raise DataException(f'Found {len(players_found)} players in slug "{slug}"; giving up')

        armies = [army for _, army in sorted(armies_found.items())] + [None] * (2 - len(armies_found))
        players = [player_id for _, player_id in sorted(players_found.items())] + [None] * (2 - len(players_found))

        return [self._merge_army_and_player(a, p) for a, p in zip(armies, players)]

    _FACTION_DATES_9TH = {
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

    @staticmethod
    def _get_edition_wh40k(army, release_date):
        # Last 9th Edition game on the channel was 2023-05-30
        if release_date > datetime.date(2023, 5, 30):
            return 10

        try:
            is_8th = release_date < ShowDataBuilder._FACTION_DATES_9TH[army.faction]
        except KeyError:
            is_8th = False

        return 8 if is_8th else 9

    _EDITION_FUNCTIONS = {
        'Warhammer 40,000': _get_edition_wh40k,
        'Age of Sigmar': lambda a, rd: 3
    }

    def get_edition(self, army, game, release_date):
        return self._EDITION_FUNCTIONS[game](army, release_date)

    def update_army_info(self, army, input_data, army_number):
        prefix = f'army{army_number}'
        player = getattr(input_data, prefix + 'player')
        faction = getattr(input_data, prefix + 'faction')

        if army:
            if player:
                try:
                    army.player_id = self._players[player]
                except KeyError:
                    raise DataException(f'Invalid player {player} supplied for army {army_number}')

            if faction:
                try:
                    army.faction_id = self._factions[faction].faction_id
                    army.faction = faction
                except KeyError:
                    raise DataException(f'Invalid faction {faction} supplied for army {army_number}')
        else:
            if player:
                try:
                    faction_id = self._factions[faction].faction_id
                except KeyError:
                    raise DataException(f'Invalid faction {faction} supplied for army {army_number}')
    
                try:
                    player_id = self._players[player]
                except KeyError:
                    raise DataException(f'Invalid player {player} supplied for army {army_number}')

                army = ArmyInfo(faction_id=faction_id, faction=faction, player_id=player_id)
            else:  
                return None

        subfaction = getattr(input_data, prefix + 'subfaction')
        if subfaction:
            try:
                army.subfaction_id = self._subfactions[subfaction].subfaction_id
            except KeyError:
                raise DataException(f'Unknown subfaction {subfaction} specified for army {army_number}')

        return army

    def set_winner(self, army1, army2, input_data):
        if input_data.winner:
            try:
                winner_id = self._players[input_data.winner]
            except KeyError:
                raise DataException(f'Unknown winner {input_data.winner} specified')
            army1.winner = army1.player_id == winner_id
            army2.winner = army2.player_id == winner_id

    def build(self, input_data):
        release_date, slug = self.parse_url(input_data.url)

        game_id, game = self.get_game(slug, input_data.game)
        showtype_id = self.get_showtype(slug, input_data.showtype)
        servoskull = input_data.servoskull
        servoskull_id = self._players[servoskull] if servoskull else None

        army1, army2 = self.extract_armies_from_slug(slug)

        army1 = self.update_army_info(army1, input_data, 1)
        army2 = self.update_army_info(army2, input_data, 2)

        self.set_winner(army1, army2, input_data)

        army1.edition = self.get_edition(army1, game, release_date)
        if army2:
            army2.edition = self.get_edition(army2, game, release_date)

        campaign = self.get_campaign_info(slug, input_data)

        showdata = ShowData(release_date, slug, input_data.youtube, game_id, showtype_id, servoskull_id, campaign, army1, army2)

        self.validate(showdata)

        return showdata

    def _validate_army(self, army, game_id):
        if army.player_id is None:
            raise ValidationException(f'Army does not have a player set')

        if game_id != self._factions_to_games[army.faction_id]:
            raise ValidationException(f'Faction {army.faction} does not belong to game ID {game_id}')

        if army.subfaction_id:
            if army.faction_id != self._subfactions_to_factions[army.subfaction_id]:
                raise ValidationException(f'Subfaction ID {army.subfaction_id} is not a subfaction of {army.faction}')

    def validate(self, showdata):
        if showdata.army1 is None:
            raise ValidationException(f'Army 1 missing')

        for army in [showdata.army1, showdata.army2]:
            if army:
                self._validate_army(army, showdata.game_id)

    @staticmethod
    def _get_episode_number_from_slug(slug):
        match = re.search(r'-ep-([0-9])-+', slug)
        return int(match.group(1)) if match else None

    def get_campaign_info(self, slug, input_data):
        if input_data.campaign is not None:
            campaign_id = self._campaigns[input_data.campaign]
        else:
            campaign_id, _ = self._get_id_from_slug(slug, self._campaigns, None)

        sequence = input_data.campaignsequence or self._get_episode_number_from_slug(slug)

        if campaign_id is not None:
            if sequence is None:
                raise DataException(f'Campaign ID {campaign_id} specified without sequence number')
            return CampaignInfo(campaign_id=campaign_id, sequence=sequence)
        else:
            return None

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

class DataException(Exception):
    pass

class ValidationException(Exception):
    pass
