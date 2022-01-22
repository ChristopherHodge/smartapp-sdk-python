from smartapp.api.smartthings import base
from smartapp.api import models
from typing import Dict, Any

RESOURCE = 'rules'

class Rule(base.APIClient):
    """Perform requests to the SmartThings Rules API.  This is intended
    to provide a fairly low level set of methods to the API functionality
    providing the serialization of the corresponding OpenAPI models, rather
    than an 'ORM-like' interface.
    """

    def __init__(self, app_id=None, **kwargs):
        self.app_id = app_id
        super().__init__(RESOURCE, **kwargs)

    async def list(self, location_id: str) -> models.smartthings.Rule:
        """List Rules

        Args:
            location_id   (str): LocationID

        Yields:
            `smartapp.api.models.smartthings.Rule`
        """
        for rule in models.smartthings.PagedRules.construct(
            **await self.do('GET', '/', params={'locationId': location_id})
        ).items:
            yield rule

    async def create(self, name: str, location_id: str,
                           action: models.smartthings.Action) -> Dict[str, Any]:
        """Create a Rule

        Args:
            name   (str): Rule Name
            location_id   (str): LocationID
            action (`smartapp.api.models.smartthings.Action`): Rule Action

        Returns:
            dict
        """
        return await self.do('POST', '/', text=models.smartthings.RuleRequest(
                name=name,
                actions=[action]
            ).json(by_alias=True, exclude_none=True), params={'locationId': location_id}
        )

    async def delete(self, location_id: str, id: str):
        """Delete a Rule

        Args:
            location_id  (str): LocationID
            id           (str): RuleID

        Returns:
            dict
        """
        return await self.do('DELETE',
            '/{}'.format(id), params={'locationId': location_id}
        )
