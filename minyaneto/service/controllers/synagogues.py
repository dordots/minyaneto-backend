import json

from flask import Blueprint, jsonify, request, current_app
from minyaneto.service.controllers.responses import no_content, bad_request
from minyaneto.service.dal.search_svc import Dao
from minyaneto.service.modules.validators import validate_synagogues
from minyaneto.utils.esjsonformat import synagogue_format

api_synagogues = Blueprint('api_synagogues', __name__)


@api_synagogues.route('/', methods=['POST'])
def add_synagogue():
    synagouge = json.loads(request.data)
    validate_synagogues(synagouge)
    dao = Dao(current_app.config['ELASTIC_SEARCH_HOSTS'])
    synagogue_id = dao.add_synagogue(synagouge)
    return jsonify({"id": synagogue_id})


@api_synagogues.route('/<id>', methods=['PUT'])
def update_synagogue(id):
    synagouge = json.loads(request.data)
    validate_synagogues(synagouge)
    dao = Dao(current_app.config['ELASTIC_SEARCH_HOSTS'])
    dao.update_synagogue(id, synagouge)
    return no_content()


@api_synagogues.route('/', methods=['GET'])
def search_synagogues():
    dao = Dao(current_app.config['ELASTIC_SEARCH_HOSTS'])
    max_hits = request.args.get('max_hits', 10)

    # option 1:
    top_left = request.args.get('top_left')
    bottom_right = request.args.get('bottom_right')

    # option 2:
    center = request.args.get('center')
    radius = request.args.get('radius')

    if center and radius:
        synagogues = dao.search_synagogues_in_circle(center, radius, max_hits=max_hits)
    elif top_left and bottom_right:
        synagogues = dao.search_synagogues_in_rectangle(top_left, bottom_right, max_hits=max_hits)
    else:
        return bad_request()

    return jsonify([synagogue_format(x) for x in synagogues])


@api_synagogues.route('/<id>', methods=['GET'])
def get_synagogue(id):
    dao = Dao(current_app.config['ELASTIC_SEARCH_HOSTS'])
    synagogue = dao.get_synagogue(id)
    return jsonify(synagogue_format(synagogue))
