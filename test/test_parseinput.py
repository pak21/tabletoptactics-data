import pytest

import tabletoptactics as tt

def test_url():
    url = 'https://tabletoptactics.tv/2023/09/26/adepta-sororitas-vs-necrons-warhammer-40k-battle-report/'
    data = f'url: {url}'

    input_data = tt.parse_input(data)

    assert input_data.url == url

def test_non_attribute():
    data = 'foo: bar'

    with pytest.raises(Exception):
        input_data = tt.parse_input(data)

def test_with_newline():
    data = 'url: foo\n'

    input_data = tt.parse_input(data)

    assert input_data.url == 'foo'
