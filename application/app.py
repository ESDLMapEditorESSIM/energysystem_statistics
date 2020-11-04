#  This work is based on original code developed and copyrighted by TNO 2020.
#  Subsequent contributions are licensed to you by the developers of such code and are
#  made available to the Project under one or several contributor license agreements.
#
#  This work is licensed to you under the Apache License, Version 2.0.
#  You may obtain a copy of the license at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#      TNO         - Initial implementation
#  Manager:
#      TNO

import logging.config

from flask import Flask, Blueprint

from application import settings
from application.api import api
from application.api.ns_statistics import ns as ns_statistics
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

# TEMPORARY SOLUTION TO DISABLE BROWSER CACHING DURING TESTING
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

def configure_app(flask_app):
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SERVER_HOST'] = settings.FLASK_SERVER_HOST
    flask_app.config['SERVER_PORT'] = settings.FLASK_SERVER_PORT
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(ns_statistics)
    flask_app.register_blueprint(blueprint)

def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://%s:%d/api/ <<<<<', settings.FLASK_SERVER_HOST, settings.FLASK_SERVER_PORT)
    app.run(host=settings.FLASK_SERVER_HOST, port=settings.FLASK_SERVER_PORT, debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()