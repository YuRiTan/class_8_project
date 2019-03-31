from flask import Flask, render_template, request
from .utils.logger import get_logger
from .statistics import ChatStats
from .etl import WhatsAppDataParser

# initialize flask application
app = Flask(__name__)
# src.config.from_envvar('secrets')
app.config['BUNDLE_ERRORS'] = True


@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("index.html")


@app.route('/upload', methods=["POST", "GET"])
def upload():
    basic_stats, users, days = "", "", ""
    if request.method == "POST":
        data = request.files["whatsapp_data"].read().decode("utf-8")
        processed_data = WhatsAppDataParser(source='stream').transform(data)
        chat_stats = ChatStats(processed_data)
        chat_stats.most_active_users()
        chat_stats.most_active_days()
        basic_stats = chat_stats.basic_statistics
        days = chat_stats.active_days
        users = chat_stats.active_users
    return render_template("upload.html", basic_stats=basic_stats, days=days, users=users)


if __name__ == '__main__':
    logger = get_logger(loglevel='DEBUG')
    # run web server
    app.run(host='0.0.0.0',
            debug=True,
            port=5555)
