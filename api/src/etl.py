import pandas as pd
import re


class WhatsAppDataParser:
    """
    Preprocessing class that transforms the file/stream input into preprocessed Pandas DataFrame
    """

    def __init__(self, source=None):
        """
        :param source: (str) either 'stream' or 'file', default: 'stream'
        """

        self.source = source if source is not None else 'stream'
        self.regex_format = None
        self.datetime_format = None

    def parse_from_stream(self, data):
        # split text on the date string that occurs at the start of every message
        return self.transform(data)

    def parse_from_file(self, path):
        with open(path, 'r') as f:
            text = f.read()
        return self.transform(text)

    def guess_regex_format(self, message_string):
        # Check if Ios format
        if message_string.startswith('['):
            message_regex = r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
            datetime_format = "%d-%m-%y %H:%M:%S"
        # Check if Android format
        elif message_string[0:2].isdigit():
            message_regex = r"(\d{2}/\d{2}/\d{4}, \d{2}:\d{2})"
            datetime_format = "%d/%m/%Y, %H:%M"
        else:
            raise ValueError("Can't recognise uploaded file content format")
        self.regex_format = message_regex
        self.datetime_format = datetime_format

    @staticmethod
    def separate_sender_from_message(df):
        df[['sender', 'message']] = df.text.str.extract("(.*?): (.*)", expand=True, flags=re.DOTALL)
        return df

    @staticmethod
    def remove_service_messages(df):
        """ separate service messages (e.g. ... has been added to group ) and regular messages """
        return df[(df.text.str.match(".*:.*")) & ~(df.text.str.match(".*Master:.*"))].reset_index(drop=False)

    def parse_and_sort_timestamp(self, df):
        df['timestamp'] = pd.to_datetime(df['timestamp'], format=self.datetime_format, yearfirst=False)
        df = df.sort_values('timestamp', ascending=True)

        return df

    @staticmethod
    def select_cols(df, cols):
        if set(cols).issubset(df.columns):
            return df.loc[:, cols]
        else:
            raise KeyError('Given cols: {} are not all in given dataframe')

    def parse_raw_text_to_df(self, data):
        self.guess_regex_format(data)
        split_messages = re.split(self.regex_format, data)
        # turn the "flat" list into a list of tuples containing the date and the text
        zipped_messages = list(zip(split_messages[1::2], split_messages[2::2]))
        return pd.DataFrame(zipped_messages, columns=['timestamp', 'text'])

    def transform(self, data):
        """ Pre processes the uploaded WhatsApp data (txt), extracts some features, and returns a dataframe.

        :param data: (str) raw input from Whatsapp chat export (txt)
        :return: (Pandas Dataframe) returns dataframe with cleaned/extracted features
        """

        return (self.parse_raw_text_to_df(data)
                .pipe(self.parse_and_sort_timestamp)
                .pipe(self.remove_service_messages)
                .pipe(self.separate_sender_from_message)
                .pipe(self.select_cols, ['sender', 'message', 'timestamp']))