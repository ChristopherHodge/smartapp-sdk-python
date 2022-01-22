from smartapp.api.smartthings import base
from smartapp.api import models
from typing import Dict, Any

RESOURCE = 'notification'

class Notification(base.APIClient):
    """Perform requests to the SmartThings Notication API.  This is intended
    to provide a fairly low level set of methods to the API functionality
    providing the serialization of the corresponding OpenAPI models, rather
    than an 'ORM-like' interface.
    """

    def __init__(self, app_id=None, **kwargs):
        self.app_id = app_id
        super().__init__(RESOURCE, **kwargs)

    async def send(self, notification) -> Dict[str, Any]:
        """Send Notification

        Args:
            notificaiton (`smartapp.api.models.smartthings.NotificationRequest`): notification

        Returns:
            dict
        """
        return await self.do('POST', '/', text=models.smartthings.NotificationRequest.parse_obj(
                notification
            ).json()
        )
