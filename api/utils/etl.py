import pandas as pd
import operator


df = pd.read_csv('utils/test_df.csv')
df['timestamp2'] = pd.to_datetime(df['timestamp2'])
df['weekday'] = df['timestamp2'].dt.weekday_name


def most_active_users():
    counts = df.sender.value_counts()
    top_senders = counts.head(5)
    result = top_senders.to_dict()
    result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    return result


def most_active_days():
    messages_per_day = df.groupby(['weekday']).count().text.to_dict()
    messages_per_day = sorted(messages_per_day.items(), key=operator.itemgetter(1), reverse=True)
    return messages_per_day

def number_of_active_members():
    return df['sender'].unique().shape[0]

def number_of_messages():
    return df.shape[0]