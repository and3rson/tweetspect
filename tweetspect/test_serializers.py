from tweetspect import serializers

class TestTweetSerializer:
    def test_serialize(self, tweets):
        serialized = serializers.Tweet(tweets, many=True)
        assert serialized.data[0]['account']['href'] == '/l33th4x'
