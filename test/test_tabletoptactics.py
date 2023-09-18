import datetime

import pytest

import tabletoptactics as tt

@pytest.fixture
def factions():
    return {
        'Space Marines': 1,
        'Chaos Space Marines': 2,
        'World Eaters': 3,
    }

@pytest.fixture
def subfactions():
    return {
        "Emperor's Children": (1, 'Chaos Space Marines', 2),
        'Dark Angels': (2, 'Space Marines', 1),
        'World Eaters': (3, 'World Eaters', 3),
    }

@pytest.mark.parametrize('unnormalized,expected',[
    ('Dark Angels', 'dark-angels'),
    ('Ulthwé', 'ulthwe'),
    ("T'au Empire", 'tau-empire'),
])
def test_normalize_for_slug(unnormalized, expected):
    normalized = tt.normalize_for_slug(unnormalized)
    assert normalized == expected

def test_extract_armies_from_slug_extracts_factions(factions, subfactions):
    slug = 'space-marines-vs-chaos-space-marines-warhammer-40000-battle-report'

    armies = tt.extract_armies_from_slug(slug, factions, subfactions)

    assert armies[0].faction_id == 1
    assert armies[0].subfaction_id is None
    assert armies[1].faction_id == 2
    assert armies[1].subfaction_id is None

def test_extract_armies_from_slug_extracts_subfactions(factions, subfactions):
    slug = 'dark-angels-vs-emperors-children-warhammer-40000-battle-report'

    armies = tt.extract_armies_from_slug(slug, factions, subfactions)

    assert armies[0].faction_id == 1
    assert armies[0].subfaction_id == 2
    assert armies[1].faction_id == 2
    assert armies[1].subfaction_id == 1

def test_extract_armies_from_slug_recognises_world_eaters_as_a_faction(factions, subfactions):
    slug = 'world-eaters-vs-space-marines-warhammer-40000-battle-report'

    armies = tt.extract_armies_from_slug(slug, factions, subfactions)

    assert armies[0].faction_id == 3
    assert armies[0].subfaction_id is None

def test_extract_armies_from_slug_throws_exception_if_no_armies_found(factions, subfactions):
    slug = 'starfleet-vs-klingons-star-trek-battle-report'

    with pytest.raises(Exception):
        armies = tt.extract_armies_from_slug(slug, factions, subfactions)

def test_extract_armies_from_slug_extracts_one_army(factions, subfactions):
    slug = 'how-to-paint-dark-angels-warhammer-40k-painting-tutorial'

    armies = tt.extract_armies_from_slug(slug, factions, subfactions)

    assert armies[0].faction_id == 1
    assert armies[0].subfaction_id == 2
    assert armies[1] is None

def test_extract_armies_from_slug_throws_exception_if_three_armies_found(factions, subfactions):
    slug = 'dark-angels-vs-emperors-children-vs-world-eaters-warhammer-40000-mega-battle-report'

    with pytest.raises(Exception):
        armies = tt.extract_armies_from_slug(slug, factions, subfactions)

def test_parse_url_parses_correctly():
    raw_url = 'https://tabletoptactics.tv/2023/09/12/world-eaters-vs-adeptus-custodes-warhammer-40k-battle-report/'

    release_date, slug = tt.parse_url(raw_url)

    assert release_date == datetime.date(2023, 9, 12)
    assert slug == 'world-eaters-vs-adeptus-custodes-warhammer-40k-battle-report'
