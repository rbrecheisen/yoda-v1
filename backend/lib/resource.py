import logging
from flask import g
from flask_restful import Resource
from lib.util import get_correlation_id


class BaseResource(Resource):

    def __init__(self):
        super(BaseResource, self).__init__()
        self._correlation_id = None
        self._logging = logging.getLogger(__name__)

    def dispatch_request(self, *args, **kwargs):
        self._correlation_id = get_correlation_id()
        return super(BaseResource, self).dispatch_request(*args, **kwargs)

    @staticmethod
    def current_user():
        return g.current_user

    def log_info(self, message):
        self._logging.info('{} {}'.format(self.correlation_id, message))

    def log_error(self, message):
        self._logging.error('{} {}'.format(self.correlation_id, message))

    def log_debug(self, message):
        self._logging.debug('{} {}'.format(self.correlation_id, message))

    def error_response(self, message, status_code):
        message = '{} {} ({})'.format(self.correlation_id, message, status_code)
        self.log_error(message)
        return {'message': message}, status_code

    @staticmethod
    def response(data, status_code=200, headers=None):
        return data, status_code, headers

    @property
    def correlation_id(self):
        return self._correlation_id
