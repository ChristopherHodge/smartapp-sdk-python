import base64
from smartapp.api import http
from smartapp.api import models

from smartapp import logger
log = logger.get()

class OAuth(http.RESTClient):

    def __init__(self):
        oauth = self.__class__.config.get('oauth')
        basic=base64.b64encode(
            '{}:{}'.format(oauth['client_id'], oauth['client_secret']
        ).encode()).decode()
        super().__init__(oauth['host'], oauth['base'], basic=basic)

    async def refresh_token(self, refresh_token):
        return models.AuthToken.parse_raw(
            await self.do('POST', '/token',
                text=models.TokenRefresh(
                    grant_type='refresh_token',
                    refresh_token=refresh_token
                ).dict()
            )
        )
