import uuid
from smartapp.api import models
from tests.conftest import test_app, client, APP_ID

initialize = models.smartapp.Configuration(
        lifecycle=models.smartapp.LifecycleType.configuration.value,
        executionId=str(uuid.uuid4()),
        locale="en",
        version="0.1.0",
        configurationData=models.smartapp.ConfigurationData(
            installedAppId=APP_ID,
            phase=models.smartapp.Phase.initialize,
            pageId="",
            previousPageId="",
            config={}
        ),
        settings={}
    )

page1 = models.smartapp.Configuration(
        lifecycle=models.smartapp.LifecycleType.configuration.value,
        executionId=str(uuid.uuid4()),
        locale="en",
        version="0.1.0",
        configurationData=models.smartapp.ConfigurationData(
            installedAppId=APP_ID,
            phase=models.smartapp.Phase.page,
            pageId="1",
            previousPageId="",
            config={
                "app": {}
            }
        ),
        settings={}
    )


def test_lifecycle_configuration_initialize():
    resp = client.post('/', data=initialize.json())
    assert resp.status_code == 200
    data = models.smartapp.ConfigurationData.parse_obj(
        resp.json()['configurationData']
    ).initialize
    app = test_app()
    assert app.permissions == data.permissions


def test_lifecycle_configuration_page1():
    resp = client.post('/', data=page1.json())
    assert resp.status_code == 200
    data = models.smartapp.ConfigurationData.parse_obj(
        resp.json()['configurationData']
    )
    app = test_app()
    assert data.page.name == app.pageId('1').page.name
