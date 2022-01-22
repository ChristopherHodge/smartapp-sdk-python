import pydantic
import traceback
from urllib import parse
from typing import Dict

from smartapp import api
from smartapp.api import models, http, types

from smartapp import logger
log = logger.get()

app_ctx = None

class SmartApp(http.RESTClient):
    """SmartApp controller"""

    @staticmethod
    async def dispatch_event(app, handler, evt):
        if handler not in app.__dir__():
            return
        handler = getattr(app, handler)
        return api.AppTask(handler, evt)

    def __init__(self, token=None):
        api = self.__class__.config.get('api')
        if not token:
            token = api.get('token')
        super().__init__(api['host'], api['base'], token=token)

    def get_ctx(self, evt: models.LifecycleBase) -> types.AppCtx:
       return types.AppCtx(
           token=evt.authToken,
           refresh_token=evt.refreshToken,
           location_id=evt.installedApp.locationId,
           app_id=evt.installedApp.installedAppId
       )

    async def handle_confirmation(self, lifecycle: models.AllLifecycles
                                  ) -> models.LifecycleResponse:
        evt = lifecycle.confirmationData
        url = parse.urlparse(evt.confirmationUrl)
        client = http.RESTClient(url.netloc, url.path, '', token=self.token)
        try:
            return models.LifecycleResponse.parse_obj(
                await client.do('GET', '?{}'.format(url.query))
            )
        except pydantic.ValidationError as e:
            log.error(traceback.format_exception(type(e), e, None))


    async def handle_configuration(self, lifecycle: models.AllLifecycles
                                   ) -> models.LifecycleResponse:
        evt = lifecycle.configurationData
        app = await app_ctx.get(evt.installedAppId)
        log.info("lifecycle: configuration: %s", evt.json())
        if evt.phase == models.smartapp.Phase.initialize:
            resp = models.LifecycleResponse(
                configurationData=app.initialize()
            )
        else:
            await getattr(app, 'lifecycle_configuration')(evt)
            resp =  models.LifecycleResponse(
                configurationData=await app.pageId(evt.pageId)
            )
        log.info("lifecycle: response: %s", resp.json())
        return resp

    async def handle_install(self, lifecycle: models.AllLifecycles
                            ) -> models.LifecycleResponse:
        evt = lifecycle.installData
        app = await app_ctx.get(evt.installedApp.installedAppId)
        app_ctx.ctx(app, self.get_ctx(evt))
        await self.dispatch_event(app, 'lifecycle_install', evt)
        return models.LifecycleResponse(
            installData={}
        )

    async def handle_uninstall(self, lifecycle: models.AllLifecycles
                              ) -> models.LifecycleResponse:
        evt = lifecycle.uninstallData
        app = await app_ctx.get(evt.installedApp.installedAppId)
        await self.dispatch_event(app, 'lifecycle_uninstall', evt)
        await app_ctx.delete(app)
        return models.LifecycleResponse(
            uninstallData={}
        )

    async def handle_update(self, lifecycle: models.AllLifecycles
                           ) -> models.LifecycleResponse:
        evt = lifecycle.updateData
        app = await app_ctx.get(evt.installedApp.installedAppId)
        app_ctx.ctx(app, self.get_ctx(evt))
        await self.dispatch_event(app, 'lifecycle_update', evt)
        return models.LifecycleResponse(
            updateData={}
        )

    async def handle_event(self, lifecycle: models.AllLifecycles
                          ) -> models.LifecycleResponse:
        evt = lifecycle.eventData
        app = await app_ctx.get(evt.installedApp.installedAppId)
        await self.dispatch_event(app, 'handle_event', evt)
        return models.LifecycleResponse(
            eventData={}
        )

    async def handle_lifecycle(self, lifecycle: models.AllLifecycles
                              ) -> models.LifecycleResponse:
        lifecycle_base = models.LifecycleBase.parse_obj(lifecycle)
        log.info("lifecycle: request: %s", lifecycle_base.json())
        handler = "handle_{}".format(lifecycle.lifecycle.lower())
        try:
            handler = getattr(self, handler)
        except AttributeError:
            return log.error("missing lifecycle handler: %s", handler)
        return await handler(lifecycle)
