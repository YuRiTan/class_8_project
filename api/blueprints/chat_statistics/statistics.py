from flask import Blueprint, jsonify
from flask import current_app as app
from utils import etl

statistics = Blueprint('statistics', __name__)

result_dict = {}
return_dict = {'status':0, 'result':{}}


@statistics.route('/whatsapi/api/v0.1/getstatistics')
def main():
    result_dict['most_active_users'] = etl.most_active_users()
    result_dict['most_active_days'] = etl.most_active_days()
    result_dict['number_of_active_members'] = etl.number_of_active_members()
    result_dict['number_of_messages'] = etl.number_of_messages()
    return_dict['status'] = 1
    return_dict['result'] = result_dict
    return jsonify(return_dict)
