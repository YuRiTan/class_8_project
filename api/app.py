from flask import Flask, jsonify, render_template, request
from utils.logger import get_logger
from statistics import ChatStats
from etl import parse_from_file, parse_from_stream

# initialize flask application
app = Flask(__name__)

app.config.from_envvar('secrets')
app.config['BUNDLE_ERRORS'] = True


@app.route('/', methods=["POST", "GET"])
def home():
    basic_stats, users, days = "", "", ""
    if request.method == "POST":
        data = request.files["whatsapp_data"].read().decode("utf-8")
        processed_data = parse_from_stream(data)
        chat_stats = ChatStats(processed_data)
        chat_stats.most_active_users()
        chat_stats.most_active_days()
        basic_stats = chat_stats.basic_statistics
        days = chat_stats.active_days
        users = chat_stats.active_users
    return render_template("index.html", basic_stats=basic_stats, days=days, users=users)


@app.route('/helloworld')
def ping():
    return jsonify(response="Hello World!"), 200


if __name__ == '__main__':
    logger = get_logger(app.config.get('LOGLEVEL'))

    # run web server
    app.run(host=app.config.get('HOST'),
            debug=app.config.get('DEBUG'),
            port=app.config.get('PORT'))
