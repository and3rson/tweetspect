import asyncio
from unittest.mock import MagicMock

import pytest

from tweetspect import twitter
from tweetspect.app import make_app

@pytest.mark.usefixtures('tweets')
class TestTweetSerializer:
    def get_application(self):
        twitter_client = MagicMock()
        destroy = asyncio.Future()
        destroy.set_result(None)
        twitter_client.destroy.return_value = destroy
        return make_app(twitter_client)

    async def test_index(self, aiohttp_client):
        client = await aiohttp_client(self.get_application())
        resp = await client.request('GET', '/')
        assert resp.status == 200
        json = await resp.json()
        assert json['success']

    def _future(self, value=None, exception=None):
        future = asyncio.Future()
        if value:
            future.set_result(value)
        if exception is not None:
            future.set_exception(exception)
        return future

    async def test_search_by_hashtag(self, aiohttp_client, tweets):
        app = self.get_application()
        client = await aiohttp_client(app)

        app['twitter_client'].fetch_by_query.return_value = self._future(value=tweets)
        resp = await client.request('GET', '/hashtags/foo')
        assert resp.status == 200
        json = await resp.json()
        assert json[0]['account']['id'] == '1337'

        app['twitter_client'].fetch_by_query.return_value = self._future(
            exception=twitter.APIError([{'code': 42, 'message': 'Boom!'}])
        )
        resp = await client.request('GET', '/hashtags/foo')
        assert resp.status == 500
        json = await resp.json()
        assert json['errors'] == ['Error 42: Boom!']

    async def test_search_by_user(self, aiohttp_client, tweets):
        app = self.get_application()
        client = await aiohttp_client(app)

        app['twitter_client'].fetch_by_user.return_value = self._future(value=tweets)
        resp = await client.request('GET', '/users/bar')
        assert resp.status == 200
        json = await resp.json()
        assert json[0]['account']['id'] == '1337'

        app['twitter_client'].fetch_by_user.return_value = self._future(
            exception=twitter.APIError([{'code': 42, 'message': 'Boom!'}])
        )
        resp = await client.request('GET', '/users/bar')
        assert resp.status == 500
        json = await resp.json()
        assert json['errors'] == ['Error 42: Boom!']
