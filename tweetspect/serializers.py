from typing import Generic, List, TypeVar

from tweetspect import twitter

T = TypeVar('T', twitter.Tweet, List[twitter.Tweet])

class Tweet(Generic[T]):
    def __init__(self, instance: T, many: bool = False):
        self.instance = instance
        self.many = many

    @property
    def data(self) -> T:
        if self.many:
            return [
                Tweet(instance).data
                for instance
                in self.instance
            ]
        return {
            'account': {
                'fullname': self.instance.user.name,
                'href': '/' + self.instance.user.screen_name,
                'id': self.instance.user.id,
            },
            'date': str(self.instance.created_at),
            'hashtags': self.instance.hashtags,
            'likes': self.instance.favorite_count,
            'replies': self.instance.reply_count,
            'retweets': self.instance.retweet_count,
            'text': self.instance.text,
        }
