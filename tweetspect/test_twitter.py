from aioresponses import aioresponses
import pytest

from tweetspect import twitter

class TestTwitterClient:
    @pytest.mark.asyncio
    async def test_auth(self):
        with aioresponses() as mock:
            mock.post('https://api.twitter.com/oauth2/token', status=200, body='{"access_token": "1337"}')
            client = twitter.TwitterClient()
            await client.ensure_token()
            assert client.access_token == '1337'
            await client.destroy()

    @pytest.mark.asyncio
    async def test_error(self):
        with aioresponses() as mock:
            mock.post(
                'https://api.twitter.com/oauth2/token',
                status=400,
                body='{"errors": [{"code": 42, "message": "Boom!"}]}'
            )
            client = twitter.TwitterClient()
            with pytest.raises(twitter.APIError, match='Error 42: Boom!'):
                await client.ensure_token()
            await client.destroy()

    @pytest.mark.asyncio
    async def test_fetch_by_query(self, search_response):
        with aioresponses() as mock:
            mock.post('https://api.twitter.com/oauth2/token', status=200, body='{"access_token": "1337"}')
            mock.get('https://api.twitter.com/1.1/search/tweets.json?count=30&q=foo', status=400, body=search_response)
            client = twitter.TwitterClient()
            results = await client.fetch_by_query('foo')
            assert results[0].user.screen_name == 'coder_487'
            assert '#RTXOn' in results[0].hashtags
            await client.destroy()

    @pytest.mark.asyncio
    async def test_fetch_by_user(self, timeline_response):
        with aioresponses() as mock:
            mock.post('https://api.twitter.com/oauth2/token', status=200, body='{"access_token": "1337"}')
            mock.get(
                'https://api.twitter.com/1.1/statuses/user_timeline.json?count=30&screen_name=bar',
                status=400,
                body=timeline_response
            )
            client = twitter.TwitterClient()
            results = await client.fetch_by_user('bar')
            assert results[0].user.screen_name == 'coder_487'
            assert '#RTXOn' in results[0].hashtags
            await client.destroy()
