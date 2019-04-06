import pandas as pd


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
            self.active_users = {k: v for k, v in result.items()}

    def most_active_days(self):
        if not hasattr(self, 'active_days'):
            self.df['weekday'] = self.df['timestamp'].dt.weekday_name
            messages_per_day = (self.df
                                .groupby(['weekday']).count()
                                .sender
                                .to_dict())
            self.active_days = messages_per_day

    def replier_count(self):
        if not hasattr(self, 'replier'):
            self.most_active_users()
            self.df['replier'] = self.df['sender'].shift(-1)
            df_agg = self.df.groupby(by=['sender', 'replier']).count()
            g = df_agg['message'].groupby(level=0, group_keys=False)
            repliers = g.nlargest(3).loc[self.df['sender'][0:2]].to_dict()
            self.replier = {"-".join([k[0], k[1]]): v
                            for k, v in repliers.items()}

    # TODO make more nice features
    def even_more_stats(self):
        pass

