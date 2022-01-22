from smartapp.api import http
from smartapp.api import models

class APIClient(http.RESTClient):

    def __init__(self, resource, token=None, session=None):
        api = self.__class__.config.get('api')
        super().__init__(api['host'], api['base'], resource, token=token, session=session)

