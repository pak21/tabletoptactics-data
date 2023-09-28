import datetime

import pytest

import tabletoptactics as tt

@pytest.fixture
def factions():
    return {
        'Space Marines': 1,
        'Chaos Space Marines': 2,
        'World Eaters': 3,
        'Astra Militarum': 4,

        'Hedonites of Slaanesh': 5,
        'Slaves to Darkness': 6,
    }

@pytest.fixture
def subfactions():
    return {
        "Emperor's Children": (1, 'Chaos Space Marines', 2),
        'Dark Angels': (2, 'Space Marines', 1),
        'World Eaters': (3, 'World Eaters', 3),
        'Slaves to Darkness': (4, 'Chaos Space Marines', 2),
    }

@pytest.fixture
def games():
    return {
        'Warhammer 40,000': 1,
    }

@pytest.fixture
def showtypes():
    return {
        'Battle report': 1,
    }

@pytest.fixture
def players():
    return {
        'Spider': 1,
        'Jinx': 2
    }

@pytest.fixture
def showdatabuilder(games, showtypes, players, factions, subfactions):
    return tt.ShowDataBuilder(games, showtypes, players, factions, subfactions)

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

def test_extract_armies_from_slug_throws_exception_if_no_armies_found(showdatabuilder):
    slug = 'starfleet-vs-klingons-star-trek-battle-report'

    with pytest.raises(Exception):
        armies = showdatabuilder.extract_armies_from_slug(slug)

def test_extract_armies_from_slug_extracts_one_army(showdatabuilder):
    slug = 'how-to-paint-dark-angels-warhammer-40k-painting-tutorial'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].faction_id == 1
    assert armies[0].subfaction_id == 2
    assert armies[1] is None

def test_extract_armies_from_slug_throws_exception_if_three_armies_found(showdatabuilder):
    slug = 'dark-angels-vs-emperors-children-vs-world-eaters-warhammer-40000-mega-battle-report'

    with pytest.raises(Exception):
        armies = showdatabuilder.extract_armies_from_slug(slug)

def test_extract_armies_from_slug_handles_chaos_space_marines(showdatabuilder):
    slug = 'astra-militarum-vs-chaos-space-marines-warhammer-40k-battle-report'

    armies = showdatabuilder.extract_armies_from_slug(slug)

    assert armies[0].faction_id == 4
    assert armies[1].faction_id == 2

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

    with pytest.raises(Exception):
        showdatabuilder.get_game(slug, games, None)

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

    with pytest.raises(Exception):
        showtype_id = showdatabuilder.get_showtype(slug, showtypes, None)

def test_get_edition_returns_3_for_age_of_sigmar(showdatabuilder):
    army = tt.ArmyInfo(faction_id=1, faction='Seraphon')
    game = 'Age of Sigmar'
    release_date = datetime.date(2023, 9, 26)

    edition = showdatabuilder.get_edition(army, game, release_date)

    assert edition == 3

def test_get_edition_returns_10_after_release_of_10th_edition(showdatabuilder):
    army = tt.ArmyInfo(faction_id=1, faction='Space Marines')
    game = 'Warhammer 40,000'
    release_date = datetime.date(2023, 9, 26)

    edition = showdatabuilder.get_edition(army, game, release_date)

    assert edition == 10

def test_get_edition_returns_9_after_9th_edition_codex_release(showdatabuilder):
    army = tt.ArmyInfo(faction_id=1, faction='Harlequins')
    game = 'Warhammer 40,000'
    release_date = datetime.date(2023, 1, 1)

    edition = showdatabuilder.get_edition(army, game, release_date)

    assert edition == 9

def test_get_edition_returns_8_before_9th_edition_codex_release(showdatabuilder):
    army = tt.ArmyInfo(faction_id=1, faction='Harlequins')
    game = 'Warhammer 40,000'
    release_date = datetime.date(2022, 1, 1)

    edition = showdatabuilder.get_edition(army, game, release_date)

    assert edition == 8

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

def test_update_army_requires_player(showdatabuilder):
    old_army = tt.ArmyInfo(faction_id=1, faction='Drukhari')

    with pytest.raises(Exception):
        new_army = showdatabuilder.update_army_info(old_army, tt.InputData(), 1)

def test_update_army_does_not_require_player_if_none(showdatabuilder):
    new_army = showdatabuilder.update_army_info(None, tt.InputData(), 1)

    assert new_army is None

def test_update_army_sets_subfaction(showdatabuilder):
    old_army = tt.ArmyInfo(faction_id=1, faction='Chaos Space Marines')
    input_data = tt.InputData(army1player='Spider', army1subfaction="Emperor's Children")

    new_army = showdatabuilder.update_army_info(old_army, input_data, 1)

    assert new_army.subfaction_id == 1

def test_update_army_creates_army(showdatabuilder):
    input_data = tt.InputData(army1player='Spider', army1faction='Chaos Space Marines')

    new_army = showdatabuilder.update_army_info(None, input_data, 1)

    assert new_army is not None
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
