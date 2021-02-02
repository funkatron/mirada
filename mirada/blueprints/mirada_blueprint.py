from flask import Blueprint, jsonify

bp = Blueprint(name=__name__, import_name='mirada_blueprint')


@bp.route('/ping')
def ping():
    return jsonify({'response': 'pong'})
