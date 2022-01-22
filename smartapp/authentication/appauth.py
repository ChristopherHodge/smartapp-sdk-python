import uuid
import enum
import random
import string
from smartapp.rest import http_error
from smartapp.api import types

PREFERENCE_LEN = 10

class AuthKeyType(enum.IntEnum):
    UUID       = enum.auto()
    PREFERENCE = enum.auto()

class AppAuth(object):

    @staticmethod
    def get_token_auth_header(req: types.AppRequest) -> str:
        auth = req.headers.get('Authorization', None)
        if not auth:
            http_error(401)
        parts = auth.split()

        if parts[0].lower() != 'bearer' or \
                len(parts) == 1 or len(parts) > 2:
            http_error(401)
        return parts[1]

    @staticmethod
    def gen_secret(key_type: AuthKeyType=AuthKeyType.UUID):
        if key_type == AuthKeyType.UUID:
            return str(uuid.uuid4())
        elif key_type == AuthKeyType.PREFERENCE:
            return str().join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=PREFERENCE_LEN
                )
            )

    def __init__(self, secret: str):
        self.secret = secret

    def authorize(self, req: types.AppRequest):
        token = self.__class__.get_token_auth_header(req)
        if not token == self.secret:
            http_error(401)
