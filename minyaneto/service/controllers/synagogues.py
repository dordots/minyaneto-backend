import json

import time
from flask import Blueprint, jsonify, request, current_app
from minyaneto.service.dal.search_svc import Dao
from minyaneto.service.modules.validators import validate_synagogues
from minyaneto.service.responses import no_content, bad_request
from minyaneto.utils.esjsonformat import synagogue_format

api_synagogues = Blueprint('api_synagogues', __name__)


@api_synagogues.route('/', methods=['POST'])
def add_synagogue():
    is_test = request.path.startswith('/test-')
    synagouge = json.loads(request.data)
    validate_synagogues(synagouge)

    # add metadata
    synagouge['_submitter_ip'] = request.remote_addr
    synagouge['_added_on'] = synagouge['_last_modified_on'] = time.time()
    synagouge['_origin'] = "app"

    dao = Dao(current_app.config['ES_HOSTS'], is_test)
    synagogue_id = dao.add_synagogue(synagouge)
    return jsonify({"id": synagogue_id})


@api_synagogues.route('/<id>', methods=['PUT'])
def update_synagogue(id):
    is_test = request.path.startswith('/test-')
    synagouge = json.loads(request.data)
    validate_synagogues(synagouge)

    # add metadata
    synagouge['_last_modified_on'] = time.time()

    # TODO: all original metadata is lost. fix this
    dao = Dao(current_app.config['ES_HOSTS'], is_test)
    dao.update_synagogue(id, synagouge)
    return no_content()


@api_synagogues.route('/', methods=['GET'])
def search_synagogues():
    is_test = request.path.startswith('/test-')
    dao = Dao(current_app.config['ES_HOSTS'], is_test)
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
    is_test = request.path.startswith('/test-')
    dao = Dao(current_app.config['ES_HOSTS'], is_test)
    synagogue = dao.get_synagogue(id)
    return jsonify(synagogue_format(synagogue))
