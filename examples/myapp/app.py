'''
This example SmartApp is purely for reference.  It has not been tested,
nor supposed to serve any functional purpose.
'''
import smartapp
from smartapp import api
from smartapp.api import task, models
from smartapp.rest import http_error

from smartapp import logger
log = logger.get()

from examples.myapp import config

class MyApp(api.SmartApp):

    @task.AppTask.handle_excs
    async def lifecycle_install(self, data):
        config = data.installedApp.config.dict()
        someDevice = config.get('someDevice')
        deviceLabel = config.get('deviceLabel')
        if deviceLabel:
            api.Device(session=self.session).update(
                someDevice, {'label': deviceLabel}
            )

    async def list_devices(self):
        async for device in api.Device(session=self.session).list():
            yield device

    @task.AppTask.handle_excs
    async def get_devices(self):
        return [device async for device \
                    in self.list_devices()]


def app():
    app = MyApp('MyApp', 'Example SmartApp')\
            .grant(scopes=['r:devices:*', 'w:devices:*', 'r:locations:*'])

    page1 = app.page('Device')
    page1.section('Device Choice')\
         .setting(name='Some Device', id='someDevice', type=api.SettingType.DEVICE)

    page2 = app.page('Label')
    page2.section('New Label')\
         .setting(name='Device Label', id='deviceLabel', type=api.SettingType.STRING)

    app.route('GET', '/devices', 'get_devices')\
            .set_auth_handler('authorize')

    return app

runner = smartapp.init(app, config)
