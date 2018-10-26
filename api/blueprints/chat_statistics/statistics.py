from flask import Blueprint, jsonify
from flask import current_app as app

statistics = Blueprint('statistics', __name__)


@statistics.route(app.config.get('api_prefix') + '/getstatistics')
def main():
    return jsonify(response="Hello World!"), 200
