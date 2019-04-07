from flask import Flask, render_template, request
import json
from utils.logger import get_logger
from statistics import ChatStats
from etl import WhatsAppDataParser

# initialize flask application
app = Flask(__name__)
# src.config.from_envvar('secrets')
app.config['BUNDLE_ERRORS'] = True


@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("index.html")


@app.route('/upload', methods=["POST", "GET"])
def upload():
    basic_stats, total_messages, active_members = {}, "", ""
    users, days, repliers, try_upload = "", "", "", False
    if request.method == "POST":
        if "whatsapp_data" not in request.files:
            return render_template("upload.html", try_upload=True)
        data = request.files["whatsapp_data"].read().decode("utf-8")
        processed_data = WhatsAppDataParser(source='stream').transform(data)
        chat_stats = ChatStats(processed_data)
        chat_stats.most_active_users()
        chat_stats.most_active_days()
        chat_stats.replier_count()
        basic_stats = chat_stats.basic_statistics
        total_messages = basic_stats.get('total_messages', None)
        active_members = basic_stats.get('active_members', None)
        days = chat_stats.active_days
        users = chat_stats.active_users
        repliers = chat_stats.replier

    return render_template("upload.html",
                           total_messages=total_messages,
                           active_members=active_members,
                           days=days,
                           users=users,
                           repliers=repliers)


if __name__ == '__main__':
    logger = get_logger(loglevel='DEBUG')
    # run web server
    app.run(host='0.0.0.0',
            debug=True,
            port=5555)
