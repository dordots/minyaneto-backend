import json

import time
from flask import Blueprint, jsonify, request, current_app
from minyaneto.service.dal.search_svc import Dao
from minyaneto.service.modules.validators import validate_synagogues
from minyaneto.service.responses import no_content, bad_request
from minyaneto.utils.esjsonformat import kehilot_format

api_kehilot = Blueprint('api_kehilot', __name__)


@api_kehilot.route('/', methods=['POST'])
def add_kehilot():
    synagouge = json.loads(request.data)
    validate_synagogues(synagouge)

    # add metadata
    synagouge['_submitter_ip'] = request.remote_addr
    synagouge['_added_on'] = synagouge['_last_modified_on'] = time.time()
    synagouge['_origin'] = "kehilot"

    dao = Dao(current_app.config['ES_HOSTS'], is_test=False)
    synagogue_id = dao.add_synagogue(synagouge)
    return jsonify({"id": synagogue_id})


@api_kehilot.route('/<id>', methods=['PUT'])
def update_kehilot(id):
    synagouge = json.loads(request.data)
    validate_synagogues(synagouge)

    # add metadata
    synagouge['_last_modified_on'] = time.time()
    synagouge['_origin'] = "kehilot"

    # TODO: all original metadata is lost. fix this
    dao = Dao(current_app.config['ES_HOSTS'], is_test=False)
    dao.update_synagogue(id, synagouge)
    return no_content()


@api_kehilot.route('/', methods=['GET'])
def search_kehilot():
    dao = Dao(current_app.config['ES_HOSTS'], is_test=False)
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

    return jsonify([kehilot_format(x) for x in synagogues])
