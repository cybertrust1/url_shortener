import pytest

from url_shortener import get_short_url, get_redirect_url
from handlers import shorten_url, redirect


@pytest.mark.parametrize('url,mojibake', [
    ('http://www.helloworld.com', '𣯷𣮮𣑥𣙬𣟷𣟲𣙤𡝣𣟭'),
    ('http://www.something.com', '𣯷𣮮𣧯𣛥𣩨𣓮𣎮𣇯𣚀'),
    (
        'https://docs.pytest.org/en/latest/parametrize.html',
        '𧉯𧇳𥝰𧳴𧋳𧨮𧟲𧎯𧋮𥟬𧃴𧋳𧨯𧡡𧥡𧛥𧩲𧓺𧊮𧑴𧛬'
    ),
    ('www.simple.com', '𣯷𣮮𣧩𣛰𣙥𡝣𣟭')
])
def test_get_short_url(url, mojibake):
    assert get_short_url(url) == mojibake


@pytest.mark.parametrize('url,mojibake', [
    ('http://www.helloworld.com', '𣯷𣮮𣑥𣙬𣟷𣟲𣙤𡝣𣟭'),
    ('http://www.something.com', '𣯷𣮮𣧯𣛥𣩨𣓮𣎮𣇯𣚀'),
    (
        'https://docs.pytest.org/en/latest/parametrize.html',
        '𧉯𧇳𥝰𧳴𧋳𧨮𧟲𧎯𧋮𥟬𧃴𧋳𧨯𧡡𧥡𧛥𧩲𧓺𧊮𧑴𧛬'
    ),
    # Missing protocol is added
    ('http://www.simple.com', '𣯷𣮮𣧩𣛰𣙥𡝣𣟭')
])
def test_get_redirect_url(url, mojibake):
    assert get_redirect_url(mojibake) == url
