from flask import Blueprint
import pandas as pd
import operator


statistics = Blueprint('statistics', __name__)

result_dict = {}
return_dict = {'status': 0, 'result': {}}


class ChatStats:
    """ Object that hold all kind of statistics for a WhatsApp group chat """

    def __init__(self, df):
        assert isinstance(df, pd.DataFrame)
        assert 'timestamp' in df.columns
        assert 'sender' in df.columns
        assert 'message' in df.columns
        self.df = df
        self.basic_statistics = self._get_basic_statistics()

    def _get_basic_statistics(self):
        return {
            'active_members': self.df['sender'].unique().shape[0],
            'total_messages': self.df.shape[0]
        }

    def most_active_users(self):
        if not hasattr(self, 'active_users'):
            counts = self.df.sender.value_counts()
            top_senders = counts.head(5)
            result = top_senders.to_dict()
            result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
            self.active_users = result

    def most_active_days(self):
        if not hasattr(self, 'active_days'):
            self.df['weekday'] = self.df['timestamp'].dt.weekday_name
            messages_per_day = self.df.groupby(['weekday']).count().sender.to_dict()
            messages_per_day = sorted(messages_per_day.items(), key=operator.itemgetter(1), reverse=True)
            self.active_days = messages_per_day

    def even_more_stats(self):
        pass

