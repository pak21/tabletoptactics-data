import datetime

import pytest

import tabletoptactics as tt

@pytest.fixture
def factions():
    return [
        (1, 'Space Marines', 1),
        (2, 'Chaos Space Marines', 1),
        (3, 'World Eaters', 1),
        (4, 'Astra Militarum', 1),

        (5, 'Hedonites of Slaanesh', 2),
        (6, 'Slaves to Darkness', 2),
    ]

@pytest.fixture
def subfactions():
    return [
        (1, "Emperor's Children", 2, 'Chaos Space Marines'),
        (2, 'Dark Angels', 1, 'Space Marines'),
        (3, 'World Eaters', 3, 'World Eaters'),
        (4, 'Slaves to Darkness', 2, 'Chaos Space Marines'),
    ]

@pytest.fixture
def games():
    return {
        'Warhammer 40,000': 1,
    }

@pytest.fixture
def showtypes():
    return {
        'Battle report': 1,
        'Narrative report': 2,
    }

@pytest.fixture
def players():
    return {
        'Spider': 1,
        'Jinx': 2
    }

@pytest.fixture
def campaigns():
    return {
        'Cinder Ark': 1,
        'The Plague War': 2,
    }

@pytest.fixture
def showdatabuilder(games, showtypes, players, campaigns, factions, subfactions):
    return tt.ShowDataBuilder(games, showtypes, players, campaigns, factions, subfactions)

@pytest.mark.parametrize('unnormalized,expected',[
    ('Dark Angels', 'dark-angels'),
    ('Ulthwé', 'ulthwe'),
    ("T'au Empire", 'tau-empire'),
])
def test_normalize_for_slug(showdatabuilder, unnormalized, expected):
    normalized = showdatabuilder.normalize_for_slug(unnormalized)
    assert normalized == expected

def test_extract_armies_from_slug_extracts_factions(showdatabuilder):
    slug = 'space-marines-vs-chaos-space-marines-warhammer-40000-battle-report'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].faction_id == 1
    assert armies[0].subfaction_id is None
    assert armies[1].faction_id == 2
    assert armies[1].subfaction_id is None

def test_extract_armies_from_slug_extracts_subfactions(showdatabuilder):
    slug = 'dark-angels-vs-emperors-children-warhammer-40000-battle-report'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].faction_id == 1
    assert armies[0].subfaction_id == 2
    assert armies[1].faction_id == 2
    assert armies[1].subfaction_id == 1

def test_extract_armies_from_slug_recognises_world_eaters_as_a_faction(showdatabuilder):
    slug = 'world-eaters-vs-space-marines-warhammer-40000-battle-report'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].faction_id == 3
    assert armies[0].subfaction_id is None

def test_extract_armies_from_slug_recognises_slaves_to_darkness_as_a_faction(showdatabuilder):
    slug = 'hedonites-of-slaanesh-vs-slaves-to-darkness-age-of-sigmar-battle-report'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].faction_id == 5
    assert armies[1].faction_id == 6

def test_extract_armies_from_slug_does_not_throw_exception_if_no_armies_found(showdatabuilder):
    slug = 'starfleet-vs-klingons-star-trek-battle-report'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0] is None
    assert armies[1] is None

def test_extract_armies_from_slug_extracts_one_army(showdatabuilder):
    slug = 'how-to-paint-dark-angels-warhammer-40k-painting-tutorial'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].faction_id == 1
    assert armies[0].subfaction_id == 2
    assert armies[1] is None

def test_extract_armies_from_slug_throws_exception_if_three_armies_found(showdatabuilder):
    slug = 'dark-angels-vs-emperors-children-vs-world-eaters-warhammer-40000-mega-battle-report'

    with pytest.raises(tt.DataException):
        armies = showdatabuilder.extract_armies_from_slug(slug)

def test_extract_armies_from_slug_handles_chaos_space_marines(showdatabuilder):
    slug = 'astra-militarum-vs-chaos-space-marines-warhammer-40k-battle-report'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].faction_id == 4
    assert armies[1].faction_id == 2

def test_extract_armies_from_slug_finds_player(showdatabuilder):
    slug = 'spiders-world-eaters-league-list-warhammer-40k-faction-focus'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].player_id == 1

def test_extract_armies_from_slug_finds_player_without_faction(showdatabuilder):
    slug = 'jinx-climbs-a-wall'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].player_id == 2
    assert armies[0].faction_id is None

def test_extract_armies_from_slug_extracts_two_players(showdatabuilder):
    slug = 'jinxs-space-marines-vs-spiders-chaos-space-marines-warhammer-40000-battle-report'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].player_id == 2
    assert armies[1].player_id == 1

def test_parse_url_parses_correctly(showdatabuilder):
    raw_url = 'https://tabletoptactics.tv/2023/09/12/world-eaters-vs-adeptus-custodes-warhammer-40k-battle-report/'

    release_date, slug = showdatabuilder.parse_url(raw_url)

    assert release_date == datetime.date(2023, 9, 12)
    assert slug == 'world-eaters-vs-adeptus-custodes-warhammer-40k-battle-report'

def test_get_game_parses_correctly(showdatabuilder):
    slug = 'space-marines-vs-orks-warhammer-40000-boarding-action-battle-report'

    game_id, game = showdatabuilder.get_game(slug, None)

    assert game_id == 1
    assert game == 'Warhammer 40,000'

def test_get_game_has_special_case_for_40k(showdatabuilder):
    slug = 'aeldari-vs-imperial-knights-warhammer-40k-battle-report'

    game_id, game = showdatabuilder.get_game(slug, None)

    assert game_id == 1
    assert game == 'Warhammer 40,000'

def test_get_game_uses_missing_value_if_unmatched(showdatabuilder):
    slug = 'space-marines-vs-orks-boarding-action-battle-report'

    game_id, game = showdatabuilder.get_game(slug, 'Warhammer 40,000')

    assert game_id == 1

def test_get_game_throws_exception_if_no_value(showdatabuilder):
    slug = 'space-marines-vs-orks-boarding-action-battle-report'

    with pytest.raises(tt.DataException):
        showdatabuilder.get_game(slug, None)

def test_get_showtype_parses_correctly(showdatabuilder):
    slug = 'aeldari-vs-imperial-knights-warhammer-40k-battle-report'

    showtype_id = showdatabuilder.get_showtype(slug, None)

    assert showtype_id == 1

def test_get_showtype_uses_missing_value_if_unmatched(showdatabuilder):
    slug = 'aeldari-vs-imperial-knights-warhammer-40k'

    showtype_id = showdatabuilder.get_showtype(slug, 'Battle report')

    assert showtype_id == 1

def test_get_showtype_throws_exception_if_unmatched(showdatabuilder):
    slug = 'aeldari-vs-imperial-knights-warhammer-40k'

    with pytest.raises(tt.DataException):
        showtype_id = showdatabuilder.get_showtype(slug, None)

def test_get_showtype_matches_crusade(showdatabuilder):
    slug = 'space-marines-vs-death-guard-the-plague-war-ep-4-warhammer-40k-crusade-report'

    showtype_id = showdatabuilder.get_showtype(slug, None)

    assert showtype_id == 2

def test_get_showtype_prefers_override_value(showdatabuilder):
    slug = 'aeldari-vs-imperial-knights-warhammer-40k-battle-report'

    showtype_id = showdatabuilder.get_showtype(slug, 'Narrative report')

    assert showtype_id == 2

def test_get_edition_returns_3_for_age_of_sigmar(showdatabuilder):
    army = tt.ArmyInfo(faction_id=1, faction='Seraphon')
    game = 'Age of Sigmar'
    release_date = datetime.date(2023, 9, 26)

    edition = showdatabuilder.get_edition(army, game, release_date, None)

    assert edition == 3

def test_get_edition_returns_10_after_release_of_10th_edition(showdatabuilder):
    army = tt.ArmyInfo(faction_id=1, faction='Space Marines')
    game = 'Warhammer 40,000'
    release_date = datetime.date(2023, 9, 26)

    edition = showdatabuilder.get_edition(army, game, release_date, None)

    assert edition == 10

def test_get_edition_returns_9_after_9th_edition_codex_release(showdatabuilder):
    army = tt.ArmyInfo(faction_id=1, faction='Harlequins')
    game = 'Warhammer 40,000'
    release_date = datetime.date(2023, 1, 1)

    edition = showdatabuilder.get_edition(army, game, release_date, None)

    assert edition == 9

def test_get_edition_returns_8_before_9th_edition_codex_release(showdatabuilder):
    army = tt.ArmyInfo(faction_id=1, faction='Harlequins')
    game = 'Warhammer 40,000'
    release_date = datetime.date(2022, 1, 1)

    edition = showdatabuilder.get_edition(army, game, release_date, None)

    assert edition == 8

def test_get_edition_honours_parameter(showdatabuilder):
    army = tt.ArmyInfo(faction_id=1, faction='Space Marines')
    game = 'Warhammer 40,000'
    release_date = datetime.date(2023, 9, 26)

    edition = showdatabuilder.get_edition(army, game, release_date, 2)

    assert edition == 2

def test_update_army_sets_army1_player(showdatabuilder):
    old_army = tt.ArmyInfo(faction_id=1, faction='Drukhari')
    input_data = tt.InputData(army1player='Spider')

    new_army = showdatabuilder.update_army_info(old_army, input_data, 1)

    assert new_army.player_id == 1

def test_update_army_set_army2_player(showdatabuilder):
    old_army = tt.ArmyInfo(faction_id=1, faction='Drukhari')
    input_data = tt.InputData(army2player='Spider')

    new_army = showdatabuilder.update_army_info(old_army, input_data, 2)

    assert new_army.player_id == 1

def test_update_army_throws_if_unknown_player(showdatabuilder):
    old_army = tt.ArmyInfo(faction_id=1, faction='Drukhari')
    input_data = tt.InputData(army1player='Grotty')

    with pytest.raises(tt.DataException):
        new_army = showdatabuilder.update_army_info(old_army, input_data, 1)

def test_update_army_does_not_require_player_if_none(showdatabuilder):
    new_army = showdatabuilder.update_army_info(None, tt.InputData(), 1)

    assert new_army is None

def test_update_army_sets_subfaction(showdatabuilder):
    old_army = tt.ArmyInfo(faction_id=1, faction='Chaos Space Marines')
    input_data = tt.InputData(army1player='Spider', army1subfaction="Emperor's Children")

    new_army = showdatabuilder.update_army_info(old_army, input_data, 1)

    assert new_army.subfaction_id == 1

def test_update_army_gives_correct_exception_if_unknown_faction(showdatabuilder):
    input_data = tt.InputData(army1player='Spider', army1faction='Dark Mechanicum')

    with pytest.raises(tt.DataException):
        army = showdatabuilder.update_army_info(None, input_data, 1)

def test_update_army_gives_correct_exception_if_unknown_subfaction(showdatabuilder):
    old_army = tt.ArmyInfo(faction_id=1, faction='Space Marines')
    input_data = tt.InputData(army1player='Spider', army1subfaction='Legion of the Damned')

    with pytest.raises(tt.DataException):
        new_army = showdatabuilder.update_army_info(old_army, input_data, 1)

def test_update_army_creates_army(showdatabuilder):
    input_data = tt.InputData(army1player='Spider', army1faction='Chaos Space Marines')

    new_army = showdatabuilder.update_army_info(None, input_data, 1)

    assert new_army is not None
    assert new_army.faction_id == 2

def test_update_army_prefers_faction_from_input_data(showdatabuilder):
    old_army = tt.ArmyInfo(faction_id=1, faction='Space Marines')
    input_data = tt.InputData(army1player='Spider', army1faction='Chaos Space Marines')

    new_army = showdatabuilder.update_army_info(old_army, input_data, 1)

    assert new_army.faction_id == 2

def test_set_winner_does_nothing_if_not_specified(showdatabuilder):
    army1 = tt.ArmyInfo(faction_id=1, faction='Space Marines')
    army2 = tt.ArmyInfo(faction_id=2, faction='Tyranids')

    showdatabuilder.set_winner(army1, army2, tt.InputData())

    assert army1.winner is None
    assert army2.winner is None

def test_sets_winner_if_specified(showdatabuilder):
    army1 = tt.ArmyInfo(faction_id=1, faction='Space Marines', player_id=1)
    army2 = tt.ArmyInfo(faction_id=2, faction='Tyranids', player_id=2)
    input_data = tt.InputData(winner='Jinx')

    showdatabuilder.set_winner(army1, army2, input_data)

    assert army1.winner == False
    assert army2.winner == True

def test_set_winner_throws_correct_exception_if_unknown_player(showdatabuilder):
    army1 = tt.ArmyInfo(faction_id=1, faction='Space Marines', player_id=1)
    army2 = tt.ArmyInfo(faction_id=2, faction='Tyranids', player_id=2)
    input_data = tt.InputData(winner='Grotty')

    with pytest.raises(tt.DataException):
        showdatabuilder.set_winner(army1, army2, input_data)

def _create_showdata(game, faction, subfaction, games, factions, subfactions):
    army1 = tt.ArmyInfo(
        player_id=1,
        faction_id=[fid for fid, f, _ in factions if f == faction][0],
        faction=faction,
        subfaction_id=[sid for sid, s, _, _ in subfactions if s == subfaction][0] if subfaction else None
    )

    return tt.ShowData(
        release_date=datetime.date(2023, 1, 1),
        slug='some-slug',
        youtube_slug=None,

        game_id=games[game],
        showtype_id=1,
        servoskull_id=None,
        campaign=None,
        league=None,

        army1=army1,
        army2=None
    )

def test_validate_does_not_throw_if_faction_matches_game(showdatabuilder, games, factions, subfactions):
    showdata = _create_showdata('Warhammer 40,000', 'Space Marines', None, games, factions, subfactions)

    showdatabuilder.validate(showdata)

    # Success is not throwing

def test_validate_throws_exception_if_faction_doesnt_match_game(showdatabuilder, games, factions, subfactions):
    showdata = _create_showdata('Warhammer 40,000', 'Hedonites of Slaanesh', None, games, factions, subfactions)

    with pytest.raises(tt.ValidationException):
        showdatabuilder.validate(showdata)

def test_validate_does_not_throw_if_subfaction_matches_faction(showdatabuilder, games, factions, subfactions):
    showdata = _create_showdata('Warhammer 40,000', 'Space Marines', 'Dark Angels', games, factions, subfactions)

    showdatabuilder.validate(showdata)

    # Success is not throwing

def test_validate_throws_exception_if_subfaction_doesnt_match_faction(showdatabuilder, games, factions, subfactions):
    showdata = _create_showdata('Warhammer 40,000', 'Chaos Space Marines', 'Dark Angels', games, factions, subfactions)

    with pytest.raises(tt.ValidationException):
        showdatabuilder.validate(showdata)

def test_validate_throws_exception_if_no_army1(showdatabuilder, games, factions, subfactions):
    showdata = _create_showdata('Warhammer 40,000', 'Space Marines', 'Dark Angels', games, factions, subfactions)
    showdata.army1 = None

    with pytest.raises(tt.ValidationException):
        showdatabuilder.validate(showdata)

def test_validate_throws_exception_if_no_player_set(showdatabuilder, games, factions, subfactions):
    showdata = _create_showdata('Warhammer 40,000', 'Space Marines', 'Dark Angels', games, factions, subfactions)
    showdata.army1.player_id = None

    with pytest.raises(tt.ValidationException):
        showdatabuilder.validate(showdata)

def test_get_campaign_returns_object_if_campaign_is_in_slug(showdatabuilder):
    slug = 'death-guard-vs-ordo-sepultura-the-plague-war-ep-3-warhammer-40k-crusade-report'

    campaign_info = showdatabuilder.get_campaign_info(slug, tt.InputData())

    assert campaign_info.campaign_id == 2
    assert campaign_info.sequence == 3

def test_get_campaign_returns_object_if_campaign_is_in_input_data(showdatabuilder):
    slug = 'dark-angels-vs-red-corsairs-warhammer-40000-narrative-report'
    input_data = tt.InputData(campaign='Cinder Ark', campaignsequence=2)

    campaign_info = showdatabuilder.get_campaign_info(slug, input_data)

    assert campaign_info.campaign_id == 1
    assert campaign_info.sequence == 2

def test_get_campaign_prefers_inputdata_if_both_are_set(showdatabuilder):
    slug = 'death-guard-vs-ordo-sepultura-the-plague-war-ep-3-warhammer-40k-crusade-report'
    input_data = tt.InputData(campaign='Cinder Ark', campaignsequence=2)

    campaign_info = showdatabuilder.get_campaign_info(slug, input_data)

    assert campaign_info.campaign_id == 1
    assert campaign_info.sequence == 2

def test_get_campaign_returns_none_if_campaign_is_not_set(showdatabuilder):
    slug = 'dark-angels-vs-red-corsairs-warhammer-40000-narrative-report'

    campaign_info = showdatabuilder.get_campaign_info(slug, tt.InputData())

    assert campaign_info is None

def test_get_campaign_throws_exception_if_campaign_specified_without_sequence(showdatabuilder):
    slug = 'dark-angels-vs-red-corsairs-warhammer-40000-narrative-report'
    input_data = tt.InputData(campaign='Cinder Ark')

    with pytest.raises(tt.DataException):
        campaign_info = showdatabuilder.get_campaign_info(slug, input_data)

def test_get_league_info_returns_none_if_league_is_not_set(showdatabuilder):
    slug = 'tau-empire-vs-death-guard-warhammer-40k-league-report'

    league_info = showdatabuilder.get_league_info(slug, tt.InputData())

    assert league_info is None

def test_get_league_info_returns_object_if_league_is_set(showdatabuilder):
    slug = 'tau-empire-vs-death-guard-warhammer-40k-league-report'
    input_data = tt.InputData(leagueseason=1, leagueepisode=2)

    league_info = showdatabuilder.get_league_info(slug, input_data)

    assert league_info.season == 1
    assert league_info.episode == 2

def test_get_league_info_returns_data_from_slug(showdatabuilder):
    slug = 'adepta-sororitas-vs-chaos-knights-warhammer-40k-league-report-s3-ep-2'

    league_info = showdatabuilder.get_league_info(slug, tt.InputData())

    assert league_info.season == 3
    assert league_info.episode == 2

def test_get_league_info_prefers_data_from_inputdata(showdatabuilder):
    slug = 'adepta-sororitas-vs-chaos-knights-warhammer-40k-league-report-s3-ep-2'
    input_data = tt.InputData(leagueseason=1, leagueepisode=4)

    league_info = showdatabuilder.get_league_info(slug, input_data)

    assert league_info.season == 1
    assert league_info.episode == 4
