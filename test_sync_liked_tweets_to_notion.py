import unittest
from unittest.mock import patch, MagicMock
from sync_liked_tweets_to_notion import MyTwitterClient, MyNotionClient


class TestMyTwitterClient(unittest.TestCase):
    @patch.object(MyTwitterClient, '__init__', return_value=None)
    def setUp(self, mock_init):
        self.twitter_client = MyTwitterClient()
        self.twitter_client.user_id = 'mocked_user_id'
        self.twitter_client.bearer_token = 'mocked_bearer_token'

    @patch('requests.get')
    def test_get_100_liked_tweets_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': 'test_data'}

        result = self.twitter_client.get_100_liked_tweets()

        self.assertEqual(result, 'test_data')

    @patch('requests.get')
    def test_get_100_liked_tweets_failure(self, mock_get):
        mock_get.return_value.status_code = 400

        with self.assertRaises(Exception):
            self.twitter_client.get_100_liked_tweets()


class TestMyNotionClient(unittest.TestCase):
    @patch.object(MyNotionClient, '__init__', return_value=None)
    def setUp(self, mock_init):
        self.notion_client = MyNotionClient()
        self.notion_client.notion_database_id = 'mocked_database_id'

    def test_tweet_exists_true(self):
        self.notion_client.client = MagicMock()
        self.notion_client.client.databases.query.return_value = {"results": ['test_data']}

        result = self.notion_client.tweet_exists('test_tweet_id')

        self.assertTrue(result)

    def test_tweet_exists_false(self):
        self.notion_client.client = MagicMock()
        self.notion_client.client.databases.query.return_value = {"results": []}

        result = self.notion_client.tweet_exists('test_tweet_id')

        self.assertFalse(result)

    def test_add_tweet_success(self):
        self.notion_client.client = MagicMock()
        self.notion_client.client.pages.create.return_value = True

        result = self.notion_client.add_tweet({'id': 'test_tweet_id', 'text': 'test_tweet_text'})

        self.assertTrue(result)

    def test_add_tweet_failure(self):
        self.notion_client.client = MagicMock()
        self.notion_client.client.pages.create.side_effect = Exception("An error occurred")

        with self.assertRaises(Exception) as context:
            self.notion_client.add_tweet({'id': 'test_tweet_id', 'text': 'test_tweet_text'})
            self.assertTrue('An error occurred' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
