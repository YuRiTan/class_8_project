import unittest
from unittest.mock import patch
from app import app
import io


class InitTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG'] = False


class TestApp(InitTest):

    def test_ping_route(self):
        response = self.app.get('/')
        self.assertIn(b'Home - Whatstats', response.data)

    def test_home_get(self):
        response = self.app.get('/upload')
        self.assertIn(b'Upload your file', response.data)

    @patch('app.ChatStats')
    def test_home_post_without_side_effects(self, ChatStats):
        ChatStats.return_value.active_users = {'Henk': a for a in range(5)}
        ChatStats.return_value.active_days = {'Bad day': a for a in range(7)}
        ChatStats.return_value.basic_statistics = {'foo': 12, 'bar': 14}

        iob_str = io.BytesIO(
            b'[22-11-13 19:08:14] Master: \xe2\x80\x8eBerichten die naar deze groep worden verzonden, zijn nu beveiligd'
            b' met end-to-end encryptie.\r\n[22-11-13 19:08:14] \xe2\x80\x8eYu heeft deze groep aangemaakt\r\n'
            b'[24-11-17 14:36:50]\xe2\x80\x8e Mi heeft Yu toegevoegd\r\n[24-11-17 14:37:22] Yu: Welkom Mi!\r\n'
        )

        response = self.app.post('/upload',
                                 content_type='multipart/form-data',
                                 data=dict(whatsapp_data=(iob_str, '../some/test_name.txt')))

        self.assertIn(b'Henk', response.data)
        self.assertIn(b'Bad day', response.data)
        self.assertIn(b'foo', response.data)




