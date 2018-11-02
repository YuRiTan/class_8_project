import unittest
from unittest.mock import patch
import pandas as pd
from app import app
from statistics import ChatStats


class InitTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()


class InitChatStat(unittest.TestCase):

    def setUp(self):
        test_dict = {
            'sender': ['Pieter', 'Maarten'],
            'message': ['Jaykie Dataleekie', 'Ik ben uit Xomnia getrapt'],
            'timestamp': [pd.to_datetime('2018-03-04 12:00:00'), pd.to_datetime('2018-03-04 16:47:23')]
        }
        data = pd.DataFrame.from_dict(test_dict)
        self.ChatStats = ChatStats(data)


class TestChatStat(InitChatStat):
    # TODO test edge-cases, perhaps tests that include failures we should cover?
    def test_basic_statistics(self):
        self.assertEqual(self.ChatStats.basic_statistics, {'active_members': 2, 'total_messages': 2})

    def test_most_active_users(self):
        self.ChatStats.most_active_users()
        self.assertEqual(set(self.ChatStats.active_users), {('Maarten', 1), ('Pieter', 1)})

    def test_most_active_days(self):
        self.ChatStats.most_active_days()
        self.assertEqual(self.ChatStats.active_days, [('Sunday', 2)])




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




