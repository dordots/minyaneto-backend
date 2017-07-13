import logging
import os
from flask import Flask, jsonify, request

from app.service.controllers.synagogues import api_synagogues


def configure_logger():
    formatter = logging.Formatter(
        '%(asctime)s (%(process)d/%(thread)d) %(filename)s:%(lineno)d %(levelname)s > %(message)s')
    app.logger.setLevel(getattr(logging, 'DEBUG'))

    # log to rotating file
    log_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'logs')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    file_handler = logging.FileHandler(os.path.join(log_directory, 'log.log'))
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    app.logger.info('Start...')


app = Flask(__name__, static_url_path='')
app.config.from_object("app.config.release.Config")
v = '/v1'
app.register_blueprint(api_synagogues, url_prefix=v + '/synagogues')
configure_logger()


@app.route('/')
def empty_root():
    return jsonify({"hello": "!"})
