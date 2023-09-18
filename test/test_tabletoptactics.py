import pytest

import tabletoptactics as tt

@pytest.mark.parametrize('unnormalized,expected',[
    ('Dark Angels', 'dark-angels'),
    ('Ulthwé', 'ulthwe'),
    ("T'au Empire", 'tau-empire'),
])
def test_normalize_for_slug(unnormalized, expected):
    normalized = tt.normalize_for_slug(unnormalized)
    assert normalized == expected
