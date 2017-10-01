"""
Three bytes in shortened URLs are designated as follows:

    0b100{bit_for_protool}{7_bits_for_a_char}{7_bits_for_a_char}

The protocol is only used by the first character. Each character encodes two
ASCII characters.
"""
from itertools import zip_longest


def get_short_url(url):
    """Return shortened form for url."""
    base = 0b100000000000000000
    if url.startswith('https://'):
        # Add the bit for https, it will stay in all characters.
        base += 0b100000000000000
        start_index = 8
    elif url.startswith('http://'):
        start_index = 7
    else:
        # URL does not have protocol, we'll add http:// to it.
        start_index = 0

    shortened_url = []
    # We will iterate URL characters in pairs and encode in a single character.
    char_pairs = zip_longest(url[start_index::2], url[start_index+1::2])
    for char1, char2 in char_pairs:
        encoded = base
        encoded += ord(char1) << 7
        # If odd number of characters, do not try to encode None.
        if char2:
            encoded += ord(char2)
        shortened_url.append(chr(encoded))
    # We join to string at the end because it is cheaper to append to a list
    # than to a string.
    return ''.join(shortened_url)


def get_redirect_url(mojibake):
    """Return decoded URL from a shortened URL."""
    decoded_url = []
    # First character (and all others) includes protocol.
    mojibake_protocol = ord(mojibake[0])
    if (mojibake_protocol >> 14) & 1:
        decoded_url.append('https://')
    else:
        decoded_url.append('http://')

    for mojibake_char in mojibake:
        mojibake_ord = ord(mojibake_char)
        ord1 = (mojibake_ord >> 7) & 127
        decoded_url.append(chr(ord1))
        ord2 = mojibake_ord & 127
        # Second character might not exist if URL has odd number of chars.
        if ord2:
            decoded_url.append(chr(ord2))
    return ''.join(decoded_url)


def validate_url(url):
    """Validate URL is correct."""
    pass
