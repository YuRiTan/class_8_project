import unittest
from unittest.mock import patch
from app import app


class InitTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()


class TestApp(InitTest):

    def test_ping_route(self):
        response = self.app.get('/helloworld')
        self.assertIn(b'Hello World', response.data)

    def test_home_get(self):
        response = self.app.get('/')
        self.assertIn(b'Upload your file', response.data)

    @patch('statistics.ChatStats')
    def test_home_post_without_side_effects(self, ChatStats):
        ChatStats.most_active_users.return_value = [('Yuri', a) for a in range(5)]
        ChatStats.most_active_days.return_value = [('Bad day', a) for a in range(7)]
        ChatStats.basic_statistics.return_value = {'foo': 12, 'bar': 14}

        f = open('../data/xomnia_chat.txt', 'rb')

        data = dict(
            whatsapp_data=f
        )
        response = self.app.post('/', content_type='multipart/form-data', data=data)
        f.close()
        print(response.data)
        self.assertTrue(True)




