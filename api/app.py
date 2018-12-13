from flask import Flask, jsonify, render_template, request
from utils.logger import get_logger
from statistics import ChatStats
from etl import parse_from_stream

# initialize flask application
app = Flask(__name__)
# app.config.from_envvar('secrets')
app.config['BUNDLE_ERRORS'] = True


@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("index.html")


@app.route('/upload', methods=["POST", "GET"])
def upload():
    print("UPLOADING")
    basic_stats, users, days = "", "", ""
    if request.method == "POST":
        print('GOT REQUEST POST:', request.files["whatsapp_data"])
        data = request.files["whatsapp_data"].read().decode("utf-8")
        processed_data = parse_from_stream(data)
        chat_stats = ChatStats(processed_data)
        chat_stats.most_active_users()
        chat_stats.most_active_days()
        basic_stats = chat_stats.basic_statistics
        days = chat_stats.active_days
        users = chat_stats.active_users
    else:
        print('ELSEIIIEEE')
    return render_template("upload.html", basic_stats=basic_stats, days=days, users=users)


@app.route('/ping')
def health_check():
    return jsonify(response="I am alive!"), 200


if __name__ == '__main__':
    logger = get_logger(loglevel='DEBUG')
    # run web server
    app.run(host='0.0.0.0',
            debug=True,
            port=5555)
