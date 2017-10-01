from url_shortener import get_short_url, get_redirect_url
import json


def shorten_url(event, context):
    url = json.loads(event.get('body'))['url']
    short_url = get_short_url(url)
    # Content-type is application/json by default, so no need to add here.
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'url': short_url
        })
    }
    return response


def redirect(event, context):
    mojibake = event['pathParameters']['mojibake']
    redirect_url = get_redirect_url(mojibake)
    response = {
        'statusCode': 302,
        'headers': {
            'Location': redirect_url,
        },
    }
    return response
