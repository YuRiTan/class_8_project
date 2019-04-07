import json
import unittest
from collections import OrderedDict

import pandas as pd
from statistics import ChatStats


class InitChatStat(unittest.TestCase):

    def setUp(self):
        test_dict = {
            'sender': ['Peter', 'Marten'],
            'message': ['Sjakie',
                        'Hoi ik ben Sjaak, maar je mag me Sjakie noemen.'],
            'timestamp': [pd.to_datetime('2018-03-04 12:00:00'),
                          pd.to_datetime('2018-03-04 16:47:23')]
        }
        data = pd.DataFrame.from_dict(test_dict)
        self.ChatStats = ChatStats(data)


class TestChatStat(InitChatStat):
    # TODO test edge-cases, perhaps tests that include failures we should cover?
    def test_basic_statistics(self):
        self.assertEqual(self.ChatStats.basic_statistics, {'active_members': 2,
                                                           'total_messages': 2})

    def test_most_active_users(self):
        self.ChatStats.most_active_users()
        exp = json.dumps(OrderedDict({'Marten': 1, 'Peter': 1}))
        self.assertEqual(self.ChatStats.active_users, exp)

    def test_most_active_days(self):
        self.ChatStats.most_active_days()
        exp = json.dumps({'Sunday': 2})
        self.assertEqual(self.ChatStats.active_days, exp)

    def test_repliers(self):
        self.ChatStats.replier_count()
        exp = json.dumps({'Peter-Marten': 1})
        self.assertEqual(self.ChatStats.replier, exp)
