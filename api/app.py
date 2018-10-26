from flask import Flask, jsonify
from utils.logger import get_logger
from blueprints.chat_statistics.statistics import statistics


# initialize flask application
app = Flask(__name__)

app.config.from_envvar('secrets')
app.config['BUNDLE_ERRORS'] = True

app.register_blueprint(statistics)


@app.route('/helloworld')
def ping():
    return jsonify(response="Hello World!"), 200


if __name__ == '__main__':
    logger = get_logger(app.config.get('LOGLEVEL'))

    # run web server
    app.run(host=app.config.get('HOST'),
            debug=app.config.get('DEBUG_MODE'),
            port=app.config.get('PORT'))