from flask import Blueprint, jsonify, request
import pandas as pd
import re

statistics = Blueprint('statistics', __name__)


@statistics.route('/whatsapi/api/v0.1/getstatistics', methods=['POST'])
def main():
    input_data = request.data.decode()
    df = pre_process_data(input_data)

    return jsonify(response="Hello World!"), 200


def pre_process_data(text):

    # split text on the date string that occurs at the start of every message
    message_regex = r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
    split_messages = re.split(message_regex, text)

    # turn the "flat" list into a list of tuples containing the date and the text
    zipped_messages = list(zip(split_messages[1::2], split_messages[2::2]))
    df = pd.DataFrame(zipped_messages, columns=['timestamp', 'text'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%y %H:%M:%S', yearfirst=False)

    # seperate service messages (e.g. ... has been added to group ) and regular messages
    df = df[df.text.str.match(".*:.*")]

    # Seperate message texts into sender and message
    df[['sender', 'message']] = df.text.str.extract("(.*?):(.*)", expand=True, flags=re.DOTALL)
    df = df.set_index('timestamp').sort_index()

    return df[['sender', 'message']]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['txt', 'json']
