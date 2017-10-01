import json
import urllib.parse
from url_shortener import (
    get_redirect_url,
    get_short_url,
)
from util import (
    is_valid_url,
    prepare_400,
)


def shorten_url(event, context):
    post_body = event.get('body')
    if not post_body:
        return prepare_400('POST body cannot be empty.')
    url = json.loads(post_body).get('url')
    if not is_valid_url(url):
        return prepare_400('url is not valid.')
    short_url = get_short_url(url)
    # Content-type is application/json by default, so no need to add here.
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'shortened_url': short_url
        })
    }
    return response


def redirect(event, context):
    mojibake = event['pathParameters']['mojibake']
    # Browsers quote non-ascii characters.
    mojibake = urllib.parse.unquote(mojibake)
    url = get_redirect_url(mojibake)
    if not is_valid_url(url):
        return prepare_400('url is not valid.')
    response = {
        'statusCode': 302,
        'headers': {
            'Location': url,
        },
    }
    return response
