from flask import Flask, jsonify, render_template, request
from utils.logger import get_logger
from blueprints.chat_statistics.statistics import statistics, get_all_statistics
from utils.etl import parse_from_file, parse_from_stream

# initialize flask application
app = Flask(__name__)

app.config.from_envvar('secrets')
app.config['BUNDLE_ERRORS'] = True

app.register_blueprint(statistics)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        data = request.files["whatsapp_data"].read().decode("utf-8")
        processed_data = parse_from_stream(data)
    return render_template("index.html")


@app.route('/helloworld')
def ping():
    return jsonify(response="Hello World!"), 200


if __name__ == '__main__':
    logger = get_logger(app.config.get('LOGLEVEL'))

    # run web server
    app.run(host=app.config.get('HOST'),
            debug=app.config.get('DEBUG'),
            port=app.config.get('PORT'))