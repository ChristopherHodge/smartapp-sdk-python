from smartapp.api.smartthings import base
from smartapp.api import models

from smartapp import logger
log = logger.get()

RESOURCE = 'scenes'

class Scene(base.APIClient):
    """class: api.Scene

    Perform requests to the SmartThings scene API.  This is intended
    to provide a fairly low level set of methods to the API functionality
    providing the serialization of the corresponding OpenAPI models, rather
    than an 'ORM-like' interface.
    """

    def __init__(self, **kwargs):
        super().__init__(RESOURCE, **kwargs)

    async def list(self):
        """Yields a scene generator, despite the function being
        async, the generator returned is not so we are blocking
        for the full response.

        Yields:
            smartapp.api.models.SceneCollection
        """
        for item in models.SceneCollection.construct(
            **await self.do('GET', '/')
        ).items:
            yield item

    async def execute(self, scene_id):
        """Execute Scene

        Args:
            scene_id (str): SceneID

        Returns:
            smartapp.api.models.RequestStatus
        """
        endpoint = '/{}/execute'.format(scene_id)
        return models.smartapp.RequestStatus.parse_obj(
            await self.do('POST', endpoint)
        )
