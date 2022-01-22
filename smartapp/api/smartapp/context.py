from __future__ import annotations
import aiohttp
from typing import Generator

from smartapp.api import models, types, smartapp
from smartapp import redis, api, authentication

from smartapp import logger
log = logger.get()

KEY_PREFIX = 'smartapp-context-'

class AppContext(redis.Redis):

    _instances = {}
    _ctx = {}
    new_app = None
    key = KEY_PREFIX + 'none'

    @classmethod
    async def get(cls, app_id: str) -> type[smartapp.SmartApp]:
        if app_id in cls._instances:
            return cls._instances[app_id]
        log.info("no app instance for app_id %s (found: %s)", app_id, cls._instances.keys())
        app = cls.new_app()
        app.ctx = cls(app_id, app)
        app.load_routes()
        return app

    @classmethod
    async def delete(cls, app: smartapp.SmartApp):
        app_id = app.app_id
        log.info("deleting app context for app_id %s", app_id)
        try:
            cls._instances.pop(app_id)
            cls._ctx.pop(app_id)
        except KeyError:
            log.info("ctx wasn't loaded for app_id %s", app_id)
        return cls().hdel(cls.key, app_id)

    @classmethod
    def store(cls, app_id: str, ctx: types.AppCtx):
        return cls().hset(cls.key, app_id, ctx.json(exclude_none=True))

    @classmethod
    def load(cls, app_id: str):
        return types.AppCtx.parse_raw(cls().hget(cls.key, app_id))

    @classmethod
    def all(cls) -> Generator[smartapp.SmartApp]:
        for app_id, instance in cls._instances:
            yield instance.app

    @classmethod
    async def init(cls) -> None:
        cls.key = KEY_PREFIX + cls.new_app().name
        for app_id in cls().hkeys(cls.key):
            app = await cls.get(app_id.decode())
            await app.lifecycle_update(
                models.smartapp.InstallData(
                    installedApp=models.smartapp.InstalledApp(
                        config={}
                    )
                )
            )

    @classmethod
    def ctx(cls, app: type[smartapp.SmartApp], ctx: types.AppCtx=None,
                 app_id: str=None) -> types.AppCtx:
        if not app_id:
            app_id = app.app_id
        if not app_id:
            raise ValueError('app_id')

        if ctx:
            log.info("updating context for app_id %s", app_id)
            cls._ctx[app_id] = ctx
            cls.store(app_id, ctx)
            app.ctx.app_ctx = ctx
            app.ctx.update_session()

        if app_id not in cls._ctx:
            log.info("no existing context for app_id %s", app_id)
            hkeys = [hkey.decode() for hkey in cls().hkeys(cls.key)]
            log.info("looking for match in stored contexts: %s", hkeys)
            if app_id in hkeys:
                log.info("loading stored context for app_id %s", app_id)
                cls._ctx[app_id] = cls.load(app_id)
            else:
                log.info("creating a new context for app_id %s", app_id)
                cls._ctx[app_id] = types.AppCtx(
                    app_id=app_id,
                    secret=authentication.AppAuth.gen_secret()
                )

        ctx = cls._ctx[app_id]
        if not ctx.secret:
            ctx.secret = authentication.AppAuth.gen_secret()
            cls.store(app_id, ctx)
        log.info("the api secret for app_id %s is %s", app_id, ctx.secret)
        return ctx

    @staticmethod
    def new_session(token: str) -> type[aiohttp.ClientSession]:
        return aiohttp.ClientSession(
            headers = {'Authorization': 'Bearer {}'.format(token)}
        )

    def __init__(self, app_id: str=None, app: smartapp.SmartApp=None):
        super().__init__()
        if not app_id or not app:
            return
        self.__class__._instances[app_id] = app
        self.app_ctx = self.__class__.ctx(app, app_id=app_id)
        self.app = app
        self._session = None
        self._auth = None

    def update_token(self, auth: models.AuthToken) -> type[AppContext]:
        self.app_ctx.token = auth.access_token
        self.app_ctx.refresh_token = auth.refresh_token
        self.__class__.ctx(self.app, ctx=self.app_ctx)

    def update_session(self):
        if self._session:
            log.info("terminating ClientSession for app_id %s", self.app_id)
            api.AppTask(self._session.close)
        log.info("instantiating new ClientSession for app_id %s with token %s", self.app_id, self.token)
        self._session = self.__class__.new_session(self.token)

    @property
    def authentication(self):
        if not self._auth:
            self._auth = authentication.AppAuth(self.secret)
        return self._auth

    @property
    def session(self) -> str:
        if not self._session:
            self.update_session()
        return self._session

    @property
    def app_id(self) -> str:
        return self.app_ctx.app_id

    @property
    def token(self) -> str:
        return self.app_ctx.token

    @property
    def refresh_token(self) -> str:
        return self.app_ctx.refresh_token

    @property
    def location_id(self) -> str:
        return self.app_ctx.location_id

    @property
    def secret(self) -> str:
        return self.app_ctx.secret
