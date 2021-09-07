import os
from typing import Tuple

def must_getenv(key: str) -> str:
    if key not in os.environ:  # pragma: no cover
        raise RuntimeError(f'Missing environment variable {key}')
    return os.getenv(key)

def get_twitter_credentials() -> Tuple[str, str]:
    return must_getenv('TWITTER_API_KEY'), must_getenv('TWITTER_API_SECRET_KEY')
