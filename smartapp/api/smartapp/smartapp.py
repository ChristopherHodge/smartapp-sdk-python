from __future__ import annotations
import random
import threading
import asyncio
from typing import List, Dict, Any, Generator

from smartapp import api
from smartapp.api import smartthings, models, types
from smartapp.api.smartapp import configuration, task

from smartapp import logger
log = logger.get()


class SmartApp(object):
    """class: SmartApp

    This class is used to define the functionality of a SmartApp.
    The instance definition of the App will be created by the
    Configuration Lifecycle, and create an instance per InstalledApp.
    """

    def __init__(self, name, st_id):
        """SmartApp: constructor

        Args:
            name (str): SmartApp appName
            descrtiption (str): SmartApp description
        """
        self.name          = name
        self.description   = name
        self.st_id         = st_id
        self.permissions   = []
        self.ctx           = None
        self.routes        = []
        self.pages         = {}
        self.configuration = {}

    @property
    def app_id(self):
        """`smartapp.api.smartapp.context.AppContext.app_id` (InstappedAppId)"""
        return self.ctx.app_id

    @property
    def location_id(self):
        """`smartapp.api.smartapp.context.AppContext.location_id` (LocationID)"""
        return self.ctx.location_id

    @property
    def session(self):
        """`smartapp.api.smartapp.context.AppContext.session` (`aiohttp.ClientSession`)
        Session to be used with SmartThings API's, provides App OAuth credentials"""
        return self.ctx.session

    @property
    def token(self):
        return self.ctx.token

    @property
    def refresh_token(self):
        return self.ctx.refresh_token

    @property
    def authentication(self):
        return self.ctx.authentication

    @task.AppTask.handle_excs
    async def lifecycle_configuration(self, data):
        self.configuration.update(
            data.config.dict()
        )
        log.info("app: configuration: %s", self.configuration)

    @task.AppTask.handle_excs
    async def lifecycle_install(self, data):
        await self.lifecycle_configuration(data.installedApp)

    @task.AppTask.handle_excs
    async def lifecycle_update(self, data):
        await self.lifecycle_install(data)

    def grant(self, scope: str = None,
                    scopes: List[str] = None) -> type[SmartApp]:
        """Add one or multiple OAuth scopes to the SmartApp requirements
        required for installation

        Args:
            scope (str): scope name
            scopes (list): scope names

        Returns:
            `SmartApp` (self)
        """
        if scopes:
            self.permissions += scopes
        else:
            self.permissions.append(scope)
        return self

    def page(self, name, pageId=None, last_page=True,
                    **kwargs) -> configuration.Page:
        """Add a new page to the Configuration Lifecycle

        Args:
            name (str): Page Name
            complete (bool): True if this is the last page

        Returns:
            `smartapp.api.smartapp.configuration.Page`: a new page

        """
        if not pageId:
            pageId = len(self.pages)
        kwargs.update({'pageId': str(pageId), 'name': name, 'complete': last_page})
        if not last_page:
            if 'nextPageId' not in kwargs:
                kwargs['nextPageId'] = str(pageId+1)
        self.pages[str(pageId)] = configuration.Page(**kwargs)
        return self.pages[str(pageId)]

    def route(self, verb: str, path: str, func: str) -> configuration.Route:
        """Register a new route for the SmartApp, the method name must
        be an async function which extends the base SmartApp class

        Args:
            verb (str): HTTP method name
            path (str): relative route URI
            func (str): function handler which extends SmartApp

        Returns:
            `smartapp.api.smartapp.configuration.Route`: the new route
        """
        route = configuration.Route(verb=verb, path=path, func=func)
        self.routes.append(route)
        return route

    async def authorize(self, req: types.AppRequest) -> bool:
        """This is a convenience method to authorize a request to
        a route handler using the instances provided smartapp.AppAuth()
        class by attaching 'authorize' as an auth handler

        example: `<route>.add_auth_handler('authorize')`

        Args:
            req (`smartapp.api.types.AppRequest`): incoming request to a SmartApp Route

        Returns:
            bool: result of auth challenge

        """
        self.authentication.authorize(req)

    @task.AppTask.handle_excs
    async def subscribe(self, type: models.SubscriptionType,
                              obj: Dict[str, List[str]] = {}) -> models.smartapp.Subscription:
        """Create subscription from the AppContext to specified source

        Args:
            type (`smartapp.api.models.SubscriptionType`): incoming request to a SmartApp Route
            obj (dict): model specified by SubscrtionType

        Returns:
            `smartapp.api.models.smartapp.Subscription`
        """

        if not isinstance(type, models.SubscriptionType):
            raise TypeError("subscribe() requires a valid SubscriptionType")

        obj.update({'subscriptionName': 's_{}'.format(
            round(random.random() * 1000000)
        ), 'stateChangeOnly': True,
           'locationId': self.location_id,
           'modes': []
        })
        if type == models.SubscriptionType.DEVICE:
            obj = {'device': obj}
        if type == models.SubscriptionType.MODE:
            obj = {'mode': obj}
        if type == models.SubscriptionType.DEVICE_LIFECYCLE:
            obj = {'deviceLifecycle': obj}
        if type == models.SubscriptionType.CAPABILITY:
            obj = {'capability': obj}
        if type == models.SubscriptionType.SCENE_LIFECYCLE:
            obj = {'sceneLifecycle': obj}
        obj.update({'sourceType': type.value})

        return await smartthings.InstalledApp(
            session=self.session, app_id=self.app_id
        ).subscribe(obj)

    @task.AppTask.handle_excs
    async def unsubscribe(self, id: str=str()) -> Dict[Any, Any]:
        """Delete subscription with ID or all subscriptions if not specified

        Args:
            id (str): SubscriptionID

        Returns:
            dict
        """

        installedapp=smartthings.InstalledApp(
            session=self.session, app_id=self.app_id
        )
        if id:
            return installedapp.ubsubscribe(id)

        coros = []
        async for item in installedapp.subscriptions():
            coros.append(installedapp.unsubscribe(item.id))
        await asyncio.wait({task.AppTask(asyncio.gather, *coros)})

    async def subscriptions(self) -> Generator[models.Subscription]:
        """List this AppContext Subscriptions

        Returns:
            `smartapp.api.models.SubscriptionCollection`
        """

        async for item in smartthings.InstalledApp(
                    session=self.session, app_id=self.app_id
                ).subscriptions():
            yield item

    @task.AppTask.handle_excs
    async def app_event(self, evt: models.smartapp.SmartAppEventRequest) -> Dict[Any, Any]:
        """Create AppEvent using current AppContext

        Args:
            evt (`smartapp.api.models.smartapp.SmartAppEventRequest`): SmartApp Event

        Returns:
            dict: Empty if success
        """
        return await smartthings.InstalledApp(
            session=self.session, app_id=self.app_id
        ).event(evt)

    @task.AppTask.handle_excs
    async def renew_token(self):
        log.info("requesting token refresh for app_id %s", self.app_id)
        try:
            resp = await smartthings.OAuth().refresh_token(self.refresh_token)
            if not resp.access_token:
                raise AssertionError(
                    resp.json(
                        include={'error': True, 'error_description': True },
                        indent=2
                    )
                )
        except types.AuthInvalid:
            return log.error("token endpoint reject the oauth client credentials")
        except AssertionError as e:
            return log.error(e)

        self.ctx.update_token(resp)

    def initialize(self) -> models.smartapp.ConfigurationData:
        self.configuration = {}
        return models.smartapp.ConfigurationData(
            initialize=models.smartapp.InitializeData(
                name=self.name,
                id=self.st_id,
                description=self.description,
                firstPageId=str(0),
                permissions=self.permissions
            )
        )

    @task.AppTask.handle_excs
    async def pageId(self, pageId: str) -> models.smartapp.ConfigurationData:
        if pageId == 0:
            self.configuration = {}

        page = self.pages[str(pageId)]

        if page.render_func:
            await page.render_func()

        return models.smartapp.ConfigurationData(
            page=page
        )

    def load_routes(self):
        for route in self.routes:
            route.app = self
            route.register()

        configuration.router.reload()
