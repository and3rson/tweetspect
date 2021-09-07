from typing import Optional

from aiohttp.web_request import Request

def get_int_param(request: Request, key: str) -> Optional[int]:
    """
    >>> import collections
    >>> from aiohttp.test_utils import make_mocked_request
    >>> request = make_mocked_request('GET', '/hashtags/foo?limit=42')
    >>> get_int_param(request, 'limit')
    42
    >>> get_int_param(request, 'foo')
    """
    try:
        return int(request.query.get(key))
    except (TypeError, ValueError):
        return None
