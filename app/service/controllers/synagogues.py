from flask import Blueprint, jsonify, request, current_app
from app.service.dal.search_svc import Dao
from app.utils.esjsonformat import synagogue_format
from decimal import Decimal

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
