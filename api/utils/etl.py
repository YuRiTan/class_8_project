import pandas as pd
import re



def parse_from_stream(data):
    # split text on the date string that occurs at the start of every message
    print(data)
    return pre_process_data(data)

def parse_from_file(path):
    with open(path, 'r') as f:
        text = f.read()
    return pre_process_data(text)


def pre_process_data(data):
    """ Pre processes the uploaded WhatsApp data (txt), extracts some features, and returns a dataframe.

    :param data: (str) raw input from Whatsapp chat export (txt)
    :return: (Pandas Dataframe) returns dataframe with cleaned/extracted features
    """
    message_regex = r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
    split_messages = re.split(message_regex, data)

    # turn the "flat" list into a list of tuples containing the date and the text
    zipped_messages = list(zip(split_messages[1::2], split_messages[2::2]))

    df = pd.DataFrame(zipped_messages, columns=['timestamp', 'text'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%y %H:%M:%S', yearfirst=False)

    # seperate service messages (e.g. ... has been added to group ) and regular messages
    df = df[df.text.str.match(".*:.*")]

    # Seperate message texts into sender and message
    df[['sender', 'message']] = df.text.str.extract("(.*?):(.*)", expand=True, flags=re.DOTALL)
    df = df.sort_values('timestamp', ascending=True)

    return df[['sender', 'message', 'timestamp']]
