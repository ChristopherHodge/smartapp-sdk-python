from smartapp.api.smartthings import base
from smartapp.api import models
from typing import Dict, Any

RESOURCE = 'installedapps'

class InstalledApp(base.APIClient):
    """Perform requests to the SmartThings InstalledApp API.  This is intended
    to provide a fairly low level set of methods to the API functionality
    providing the serialization of the corresponding OpenAPI models, rather
    than an 'ORM-like' interface.
    """

    def __init__(self, app_id=None, **kwargs):
        self.app_id = app_id
        super().__init__(RESOURCE, **kwargs)

    async def list(self) -> models.InstalledAppCollection:
        """List InstalledApp's

        Returns:
            `smartapp.api.models.InstalledAppCollection`
        """
        return models.InstalledAppCollection.parse_obj(
            await self.do('GET', '/')
        )

    async def subscriptions(self, app_id=None) -> models.SubscriptionCollection:
        """Get Subscriptions belonging to app_id

        Args:
            app_id (str): Not needed if invoked via `smartapp.api.smartapp.smartapp.SmartApp.subscriptions`

        Yields:
            `smartapp.api.models.Subscription`
        """
        if not app_id:
            if not self.app_id:
                raise ValueError('app_id')
            app_id = self.app_id
        for item in models.SubscriptionCollection.parse_obj(
            await self.do(
                'GET', '/' + app_id + '/subscriptions'
            ) or {'items': []}
        ).items:
            yield item

    async def subscribe(self, data: models.smartthings.SubscriptionRequest,
                              app_id=None) -> models.smartthings.Subscription:
        """Create a new SmartThings Event Subscription for the SmartApp.  Received events
        are passed to the SmartApp's 'handle_event(SubscriptionEvent)' method, which you
        must define.

        Args:
            req (`smartapp.api.models.smartthings.SubscriptionRequest`): new subscription request
            app_id (str): Not needed if invoked via `smartapp.api.smartapp.smartapp.SmartApp.subscribe`

        Returns:
            `smartapp.api.models.smartthings.Subscription`

        """
        if not app_id:
            if not self.app_id:
                raise ValueError('app_id')
            app_id = self.app_id
        return models.smartthings.Subscription.parse_obj(
            await self.do('POST', '/' + app_id + '/subscriptions',
                models.smartthings.SubscriptionRequest.parse_obj(data).dict()
            )
        )

    async def unsubscribe(self, id, app_id=None):
        """Delete an existing Subscription

        Args:
            req (UnsubscribeRequest): unsubscribe request
            app_id (str): Not needed if invoked via `smartapp.api.smartapp.smartapp.SmartApp.unsubscribe`

        Returns:
            dict

        """
        if not app_id:
            if not self.app_id:
                raise ValueError('app_id')
            app_id = self.app_id
        return await self.do(
            'DELETE', '/' + app_id + '/subscriptions/' + id
        )

    async def event(self, data: models.smartthings.SmartAppEventRequest,
                          app_id: str = None) -> Dict[str, Any]:
        """Send an AppEvent

        Args:
            evt (`smartapp.api.models.smartthings.InstalledAppEventRequest`): List of SmartAppEventeRequest
            app_id (str): Not needed if invoked via `smartapp.api.smartapp.smartapp.SmartApp.app_event`

        Returns:
            dict
        """
        if not app_id:
            if not self.app_id:
                raise ValueError('app_id')
            app_id = self.app_id
        return await self.do('POST', '/' + app_id + '/events',
            models.smartthings.CreateInstalledAppEventsRequest(
                smartAppEvents=[
                    models.smartthings.SmartAppEventRequest.parse_obj(
                        data
                    )
                ]
            ).dict()
        )
