import json
import urllib.parse


def prepare_400(message):
    """Shortcut method for preparing 400 responses."""
    response = {
        'statusCode': 400,
        'body': json.dumps({
            'message': message
        })
    }
    return response


def is_valid_url(url):
    """Validate URL to have protocol and netloc."""
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    return True
