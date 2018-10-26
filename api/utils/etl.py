import operator


def most_active_users(df):
    counts = df.sender.value_counts()
    top_senders = counts.head(5)
    result = top_senders.to_dict()
    result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    return result


def most_active_days(df):
    df['weekday'] = df['timestamp'].dt.weekday_name
    messages_per_day = df.groupby(['weekday']).count().sender.to_dict()
    messages_per_day = sorted(messages_per_day.items(), key=operator.itemgetter(1), reverse=True)
    return messages_per_day


def number_of_active_members(df):
    return df['sender'].unique().shape[0]


def number_of_messages(df):
    return df.shape[0]