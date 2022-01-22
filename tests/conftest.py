import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import asyncio
import pytest
from fastapi.testclient import TestClient

import smartapp
from smartapp import main
from smartapp.api import models

from tests import test_config
from  redis import UnixDomainSocketConnection
import redislite

APP_ID = "2222222b-bbbb-cccc-1111-dddddddddddd"

client = TestClient(main.app)
main.include_routes()

test_config.smartthings = {
    'api': {
        'scheme': 'http',
        'host': 'api.host.name',
        'base': '/test',
        'token': 'test-token'
    }
}

@pytest.fixture(autouse=True)
def with_redis():
    redis = redislite.Redis()
    redis_sock = redis.socket_file

    test_config.redis = {
        'connection_class': UnixDomainSocketConnection,
        'path': redis_sock
    }

    yield redis

    redis.shutdown()


class AppTestApp(smartapp.api.smartapp.SmartApp):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_route1(self):
        return {'name': 'test_route1'}

    async def test_route1_slug(self, slug):
        return {'slug': slug}

    async def test_route1_body(self, item: models.smartapp.Settings):
        return {'body': item}


def test_app():
    app = AppTestApp('TestApp', 'Test SmartApp')\
            .grant(scopes=['r:devices:*', 'w:devices:*', 'r:locations:*'])

    page1 = app.page('Test Page 1')

    page1.section('Device Choice')\
         .setting(name='Test Device',
                  id='testDeice',
                  type=smartapp.api.SettingType.DEVICE)

    page1.section('Setting1 Section')\
        .setting(name='Setting', id='setting', type=smartapp.api.SettingType.ENUM)\
        .has_multiple(True)\
        .option('test1', 'value1')\
        .option('test1', 'value2')

    app.route('GET',  '/route1',         'test_route1')
    app.route('GET',  '/route1/{slug}',  'test_route1_slug')
    app.route('POST', '/route1',         'test_route1_body')
    app.route('GET',  '/allow',          'test_route1')
    app.route('GET',  '/require_auth',   'test_route1')\
            .set_auth_handler('authorize')

    return app

smartapp.init(test_app, test_config)
