from aiohttp import web

from tweetspect import serializers, twitter
from tweetspect.utils import get_int_param

async def search_by_hashtag(request: web.Request) -> web.Response:
    limit = get_int_param(request, 'limit')
    twitter_client = request.app['twitter_client']
    try:
        tweets = await twitter_client.fetch_by_query(
            '#' + request.match_info['hashtag'], limit
        )
    except twitter.APIError as exc:
        return web.json_response(dict(errors=exc.errors), status=500)
    return web.json_response(serializers.Tweet(tweets, many=True).data)

async def search_by_user(request: web.Request) -> web.Response:
    limit = get_int_param(request, 'limit')
    twitter_client = request.app['twitter_client']
    try:
        tweets = await twitter_client.fetch_by_user(
            request.match_info['username'], limit
        )
    except twitter.APIError as exc:
        return web.json_response(dict(errors=exc.errors), status=500)
    return web.json_response(serializers.Tweet(tweets, many=True).data)
