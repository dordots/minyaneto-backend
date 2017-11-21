import json

from flask import Blueprint, jsonify, request, current_app
from decimal import Decimal

from minyaneto.service.controllers.responses import no_content
from minyaneto.service.dal.search_svc import Dao
from minyaneto.utils.esjsonformat import synagogue_format

api_synagogues = Blueprint('api_synagogues', __name__)



@api_synagogues.route('/', methods=['POST'])
def add_synagogue():
    synagouge = json.loads(request.data)
    dao = Dao(current_app.config['ELASTIC_SEARCH_HOSTS'])
    synagogue_id = dao.add_synagogue(synagouge)
    return jsonify({"id": synagogue_id})


@api_synagogues.route('/<id>', methods=['PUT'])
def update_synagogue(id):
    synagouge = json.loads(request.data)
    dao = Dao(current_app.config['ELASTIC_SEARCH_HOSTS'])
    dao.update_synagogue(id, synagouge)
    return no_content()


@api_synagogues.route('/', methods=['GET'])
def get_synagogues():
    max_hits = request.args.get('max_hits', 10)
    tl = request.args.get('top_left').split(',')
    top_left = {'lat': Decimal(tl[0]), 'lon': Decimal(tl[1])}
    br = request.args.get('bottom_right').split(',')
    bottom_right = {'lat': Decimal(br[0]), 'lon': Decimal(br[1])}

    dao = Dao(current_app.config['ELASTIC_SEARCH_HOSTS'])
    synagogues = dao.search_synagogues(top_left, bottom_right, max_hits=max_hits)
    return jsonify({"synagogues": [synagogue_format(x) for x in synagogues]})


@api_synagogues.route('/<id>', methods=['GET'])
def get_synagogue(id):
    dao = Dao(current_app.config['ELASTIC_SEARCH_HOSTS'])
    synagogue = dao.get_synagogue(id)
    return jsonify({"synagogue": synagogue_format(synagogue)})