from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from aiohttp import BasicAuth, ClientSession
from aiohttp.client_reqrep import ClientResponse
from pydantic import BaseModel, validator

from tweetspect import settings

class User(BaseModel):
    id: str
    name: str
    screen_name: str

class Hashtag(BaseModel):
    text: str
    indices: Tuple[int, int]

class Entities(BaseModel):
    hashtags: List[Hashtag]

class Tweet(BaseModel):
    user: User
    created_at: datetime
    entities: Entities
    favorite_count: int
    reply_count: int = -1
    retweet_count: int
    text: str

    @validator('created_at', pre=True)
    def time_validate(cls, value: Union[datetime, str]) -> datetime:  # pylint: disable=no-self-argument
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, '%a %b %d %H:%M:%S +0000 %Y')

    @property
    def hashtags(self) -> List[str]:
        return [
            '#' + hashtag.text
            for hashtag
            in self.entities.hashtags
        ]

class APIError(Exception):
    def __init__(self, errors: List[Dict]):
        self.errors = [
            f'Error {error["code"]}: {error["message"]}'
            for error
            in errors
        ]
        super().__init__(self, '\n'.join(self.errors))

class TwitterClient:
    API_ROOT = 'https://api.twitter.com'

    def __init__(self):
        self._session = None
        self.access_token = None

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession()
        return self._session

    async def ensure_token(self) -> None:
        if self.access_token is None:
            response = await self.session.post(
                f'{self.API_ROOT}/oauth2/token',
                auth=BasicAuth(*settings.get_twitter_credentials()),
                data=dict(
                    grant_type='client_credentials',
                )
            )
            body = await response.json()
            self._validate_response_body(body)
            self.access_token = body['access_token']

    def _validate_response_body(self, response: ClientResponse) -> None:
        if 'errors' in response:
            raise APIError(**response)

    async def _get(self, url: str, **params) -> Optional[Union[List, Dict, int, str]]:
        response = await self.session.get(
            url,
            headers={
                'Authorization': f'Bearer {self.access_token}',
            },
            params=params,
        )
        body = await response.json()
        self._validate_response_body(body)
        return body

    async def fetch_by_query(self, query: str, limit: Optional[int] = None) -> List[Tweet]:
        if limit is None:
            limit = 30
        await self.ensure_token()
        body = await self._get(
            f'{self.API_ROOT}/1.1/search/tweets.json',
            q=query,
            count=limit
        )
        return [Tweet.parse_obj(data) for data in body['statuses']]

    async def fetch_by_user(self, screen_name: str, limit: Optional[int] = None) -> List[Tweet]:
        if limit is None:
            limit = 30
        await self.ensure_token()
        body = await self._get(
            f'{self.API_ROOT}/1.1/statuses/user_timeline.json',
            screen_name=screen_name,
            count=limit
        )
        return [Tweet.parse_obj(data) for data in body]

    async def destroy(self) -> None:
        await self.session.close()
