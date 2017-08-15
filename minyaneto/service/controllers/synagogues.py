from flask import Blueprint, jsonify, request, current_app
from decimal import Decimal

from minyaneto.service.dal.search_svc import Dao
from minyaneto.utils.esjsonformat import synagogue_format

api_synagogues = Blueprint('api_synagogues', __name__)


@api_synagogues.route('/', methods=['GET'])
def get_synagogues():
    tl = request.args.get('top_left').split(',')
    top_left = {'lat': Decimal(tl[0]), 'lon': Decimal(tl[1])}
    br = request.args.get('bottom_right').split(',')
    bottom_right = {'lat': Decimal(br[0]), 'lon': Decimal(br[1])}

    dao = Dao(current_app.config['ELASTIC_SEARCH_HOSTS'],
              current_app.config['ELASTIC_SEARCH_PORT'],
              current_app.config['ELASTIC_SEARCH_USER'],
              current_app.config['ELASTIC_SEARCH_PASS'])
    synagogues = dao.search_synagogues(top_left, bottom_right)
    return jsonify({"synagogues": [synagogue_format(x) for x in synagogues]})