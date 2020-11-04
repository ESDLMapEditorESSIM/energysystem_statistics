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

import logging
import urllib
from application.statistics import es_statistics
from flask import request
from flask_restplus import Resource, fields
from application.api import api
import json

log = logging.getLogger(__name__)

ns = api.namespace('statistics', description='Operations to calculate energy system statistics')


post_body = api.model('PostBody', {
    'energysystem': fields.String
})


@ns.route('/calculate', methods=['POST'])
class StatisticsPost(Resource):

    @api.expect(post_body)
    def post(self):
        post_body = json.loads(request.get_data().decode("utf-8"))
        esdl_string = urllib.parse.unquote(post_body["energysystem"])
        stats = es_statistics.EnergySystemStatistics()
        return stats.calculate(esdl_string)
