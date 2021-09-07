from aiohttp import web

from tweetspect import twitter, views

async def index(_) -> web.Response:
    return web.json_response(dict(success=True))

def make_app(twitter_client: twitter.TwitterClient) -> web.Application:
    application = web.Application()
    application.add_routes([web.get('/', index)])
    application.add_routes([web.get(r'/hashtags/{hashtag:\w+}', views.search_by_hashtag)])
    application.add_routes([web.get(r'/users/{username:\w+}', views.search_by_user)])

    async def app_startup(application):
        application['twitter_client'] = twitter_client

    async def app_cleanup(application):
        await application['twitter_client'].destroy()

    application.on_startup.append(app_startup)
    application.on_cleanup.append(app_cleanup)
    return application

app = make_app(twitter.TwitterClient())

if __name__ == '__main__':  # pragma: no cover
    web.run_app(app)
