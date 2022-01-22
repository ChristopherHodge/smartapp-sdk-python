from smartapp.api.smartthings import base
from smartapp.api import models

from smartapp import logger
log = logger.get()

RESOURCE = 'devices'

class Device(base.APIClient):
    """class: api.Device

    Perform requests to the SmartThings device API.  This is intended
    to provide a fairly low level set of methods to the API functionality
    providing the serialization of the corresponding OpenAPI models, rather
    than an 'ORM-like' interface.
    """

    def __init__(self, **kwargs):
        super().__init__(RESOURCE, **kwargs)

    async def list(self):
        """Yields a device generator, despite the function being
        async, the generator returned is not so we are blocking
        for the full response.

        Yields:
            smartapp.api.models.DeviceCollection
        """
        for item in models.DeviceCollection.construct(
            **await self.do('GET', '/')
        ).items:
            yield item

    async def get(self, device_api_id):
        """ Return the Device

        Args:
            device_api_id (str): SmartThings DeviceID

        Returns:
            smartapp.api.models.smartthings.Device
        """
        return models.smartthings.Device.parse_obj(
            await self.do('GET', '/{}'.format(device_api_id))
        )

    async def status(self, device_api_id):
        """ Return the DeviceStatus

        Args:
            device_api_id (str): SmartThings DeviceID

        Returns:
            smartapp.api.models.smartthings.DeviceStatus
        """
        return models.smartthings.DeviceStatus.parse_obj(
            await self.do('GET', '/{}/status'.format(device_api_id))
        )

    async def get_component(self, device_api_id, component_id):
        """ Return the Device ComponentStatus

        Args:
            device_api_id (str): SmartThings DeviceID
            component_id (str): SmartThings Device ComponentID

        Returns:
            smartapp.api.models.smartthings.ComponentStatus
        """
        return models.smartthings.ComponentStatus.parse_obj(
            await self.do('GET',
                '/{}/components/{}/status'.format(device_api_id, component_id)
            )
        )

    async def create(self, app_id, location_id, profile_id, label):
        """Use the SmartApp auth to create a device, with itself as
        the owner.

        Args:
            app_id (str): InstalledAppId
            location_id (str): LocationID
            profile_id (str): ProfileID
            label (str): Device Label

        Returns:
            smartapp.api.models.smartthings.Device
        """
        return models.smartthings.Device.parse_obj(
            await self.do('POST', '/',
                models.smartthings.DeviceInstallRequest(
                    app=models.smartthings.App(
                        profileId=profile_id,
                        installedAppId=app_id
                    ),
                    locationId=location_id,
                    label=label
                ).dict()
            )
        )

    async def event(self, device_api_id, event):
        """Send an event for a device to the device event endpoint.
        Uses SmartApp auth which must also be the device owner.

        Args:
            device_id (str): SmartThings DeviceID
            event (DeviceEventRequest): Device Event model

        Returns:
            dict
        """
        path = '/{}/events'.format(device_api_id)
        return await self.do('POST', path,
            models.smartthings.DeviceEventsRequest(
                deviceEvents=[
                    models.smartthings.DeviceStateEvent.parse_obj(event)
                ]
            ).dict()
         )

    async def command(self, device_api_id, cmd):
        """Send a command for a device to the device commands endpoint.
        Uses SmartApp auth which must also be the device owner.

        Args:
            device_id (str): SmartThings DeviceID
            cmd (DeviceCommand): Device Command model

        Returns:
            dict
        """
        path = '/{}/commands'.format(device_api_id)
        return await self.do('POST', path,
            models.smartthings.DeviceCommandsRequest(
                commands=[
                    models.smartthings.DeviceCommand.parse_obj(cmd)
                ]
            ).dict()
         )

    async def update(self, device_api_id, update):
        """Update a device entry

        Args:
            device_api_id (str): DeviceID
            update (str): UpdateDeviceRequest

        Return:
            smartapp.api.models.smartthings.Device
        """
        return models.smartthings.Device.parse_obj(
            await self.do('PUT', '/{}'.format(device_api_id),
                models.smartthings.UpdateDeviceRequest.parse_obj(
                    update
                ).dict()
            )
        )
