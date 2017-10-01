import json
import pytest
import urllib.parse

from handlers import shorten_url, redirect
from url_shortener import get_short_url, get_redirect_url
from util import prepare_400, is_valid_url


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


@pytest.mark.parametrize('message', [
    'some 400 message',
    'bad request'
])
def test_prepare_400(message):
    response = prepare_400(message)
    assert response == {
        'statusCode': 400,
        'body': '{{"message": "{}"}}'.format(message)
    }


@pytest.mark.parametrize('url,valid_or_not', [
    ('no_protocol.com', False),
    ('www.no_protocol.com', False),
    ('http://', False),
    ('http://www.example.com', True),
    ('http://www.com', True),
    ('https://www.com', True),
])
def test_is_valid_url(url, valid_or_not):
    url_valid = is_valid_url(url)
    assert url_valid == valid_or_not


@pytest.mark.parametrize('url,mojibake', [
    ('http://www.helloworld.com', '𣯷𣮮𣑥𣙬𣟷𣟲𣙤𡝣𣟭'),
    ('http://www.something.com', '𣯷𣮮𣧯𣛥𣩨𣓮𣎮𣇯𣚀'),
    (
        'https://docs.pytest.org/en/latest/parametrize.html',
        '𧉯𧇳𥝰𧳴𧋳𧨮𧟲𧎯𧋮𥟬𧃴𧋳𧨯𧡡𧥡𧛥𧩲𧓺𧊮𧑴𧛬'
    ),
])
def test_shorten_url(url, mojibake):
    event = {
        'body': '{{"url": "{}"}}'.format(url)
    }
    response = shorten_url(event, None)
    assert response == {
        'statusCode': 200,
        'body': '{{"shortened_url": {}}}'.format(
            json.dumps(mojibake)
        )
    }


@pytest.mark.parametrize('url', [
    'www.simple.com',
    'invalid_url',
])
def test_shorten_url_invalid_url(url):
    event = {
        'body': '{{"url": "{}"}}'.format(url)
    }
    response = shorten_url(event, None)
    assert response == prepare_400('url is not valid.')


def test_shorten_url_empty_body():
    response = shorten_url({}, None)
    assert response == prepare_400('POST body cannot be empty.')


@pytest.mark.parametrize('url,mojibake', [
    ('http://www.helloworld.com', '𣯷𣮮𣑥𣙬𣟷𣟲𣙤𡝣𣟭'),
    ('http://www.something.com', '𣯷𣮮𣧯𣛥𣩨𣓮𣎮𣇯𣚀'),
    (
        'https://docs.pytest.org/en/latest/parametrize.html',
        '𧉯𧇳𥝰𧳴𧋳𧨮𧟲𧎯𧋮𥟬𧃴𧋳𧨯𧡡𧥡𧛥𧩲𧓺𧊮𧑴𧛬'
    ),
])
def test_redirect(url, mojibake):
    event = {
        'pathParameters': {
            'mojibake': urllib.parse.quote(mojibake)
        }
    }
    response = redirect(event, None)
    assert response == {
        'statusCode': 302,
        'headers': {
            'Location': url
        }
    }
