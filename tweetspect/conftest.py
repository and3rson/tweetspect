from datetime import datetime
import os
from typing import List

import pytest

from tweetspect import twitter

THIS_DIR = os.path.dirname(__file__)

@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv('TWITTER_API_KEY', 'foo')
    monkeypatch.setenv('TWITTER_API_SECRET_KEY', 'bar')

@pytest.fixture()
def search_response() -> str:
    with open(os.path.join(THIS_DIR, './tests/search_response.json'), 'r', encoding='utf-8') as fobj:
        return fobj.read()

@pytest.fixture()
def timeline_response() -> str:
    with open(os.path.join(THIS_DIR, './tests/timeline_response.json'), 'r', encoding='utf-8') as fobj:
        return fobj.read()

@pytest.fixture()
def tweets() -> List[twitter.Tweet]:
    return [
        twitter.Tweet(
            user=twitter.User(
                id='1337',
                name='L33t H4x',
                screen_name='l33th4x',
            ),
            created_at=datetime(year=2000, month=1, day=1),
            entities=twitter.Entities(
                hashtags=[
                    twitter.Hashtag(text='test', indices=[10, 14]),
                ],
            ),
            favorite_count=3,
            retweet_count=4,
            text='This is a #test',
        ),
        twitter.Tweet(
            user=twitter.User(
                id='1338',
                name='L33t H4x 2',
                screen_name='l33th4x 2',
            ),
            created_at=datetime(year=2000, month=1, day=2),
            entities=twitter.Entities(
                hashtags=[],
            ),
            favorite_count=3,
            retweet_count=4,
            text='This is another test',
        ),
    ]
