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

from flask_restplus import Api
from flask_restplus import reqparse
from application import settings

log = logging.getLogger(__name__)

api = Api(version='0.1', title='Energy system statistics service',
          description='A first implementation of a service that calculates different kind of statistics for the energy system')
#
# pagination_arguments = reqparse.RequestParser()
# pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
# pagination_arguments.add_argument('bool', type=bool, required=False, default=1, help='Page number')
# pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
#                                   default=10, help='Results per page {error_msg}')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
